import os
import sys
import tempfile
import subprocess
import json

import pprint
import rasterio
from rasterio import features
from shapely.geometry import asShape

COLORS = {
    'little': '#189613', 
    'low': '#eff023', 
    'moderate': '#e0b211', 
    'high': '#e76b08', 
    'peak' : '#b52a29', 
    'past': '#634e1d'
}
    
if __name__ == '__main__':
    
    in_filename = sys.argv[1]
    out_filename = os.path.splitext(in_filename)[0] + '_composite.tif'

    for (i, (level, color)) in enumerate(COLORS.items()):
        working_dir = os.getcwd() + '/work'        
        scratch_file = working_dir + '/extract_' + str(i) + '.tif'
        path_to_mask_file = os.getcwd() + '/mask.png'

        # mask out the surrounding text and, most importantly, the map legend
        subprocess.call(['convert', in_filename, path_to_mask_file, '-alpha', 'Off', '-compose', 'CopyOpacity', '-colorspace', 'sRGB', '-composite', scratch_file])

        # pull out the single color we're currently looking for
        subprocess.call(['mogrify', '-fill', 'transparent', '-fuzz', '10%', '+opaque', color, scratch_file])
        # this might be redundant, but I don't know GDAL well enough to know
        # subprocess.call(['mogrify', '-fill', 'Off', '-fuzz', '10%', '+opaque', color, scratch_file])        

        # get rid of the black
        subprocess.call(['mogrify', '-transparent', '#000000', scratch_file])

        # convert everything to a single color for feature extraction
        subprocess.call(['mogrify', '-fill', 'red', '-fuzz', '10%', '-opaque', color, scratch_file])

        # apply georeferencing
        subprocess.call(['sh', os.getcwd() + '/georeference.sh', scratch_file])
        
        # create geoJSON
        j = json.loads(subprocess.check_output(['rio', 'shapes', '--mask', scratch_file]))
        
        # buffer objects
        for (i, shape) in enumerate(j['features']):
            shapely_shape = asShape(shape['geometry'])
            j['features'][i]['geometry']['coordinates'] = list(shapely_shape.buffer(100).exterior.coords)


        f = open(working_dir + '/shapes_' + str(i) + '.geojson', 'w')        
        f.write(json.dumps(j))
        f.close()


        # with rasterio.open(scratch_file) as src:
        #     alpha_band = src.read_band(1)
        #     mask = alpha_band != 255
        #     shapes = features.shapes(alpha_band, mask)    
        
        # j = {
        #     'type': 'FeatureCollection',
        #     'features': []
        # }
        # for s in shapes:
        #     j['features'].append(s)        

        # f = open('work/gj_' + str(i) + '.geojson', 'w')
        # f.write(json.dumps(j))
        # f.close()


        # #     alpha_band = src.read_band(1)
        
        #     mask = alpha_band != 255
        #     shapes = features.shapes(alpha_band, mask=mask)
            
        #     for s in shapes:
        #         print json.dumps({'features': [{'type': 'Feature', 'geometry': s}] }, indent=2)

        #     image = features.rasterize(((g, 255) for g, v in shapes), out_shape=src.shape)

        # with rasterio.open('{working_dir}/rasterio_{i}.tif'.format(working_dir=working_dir, i=i), 'w',
        #     driver='GTiff',
        #     dtype=rasterio.uint8,
        #     count=1,
        #     width=src.width,
        #     height=src.height) as dst:
            
        #     dst.write_band(1, image)


        # view results
        # subprocess.call(['open', scratch_file])
    
        # os.removedirs(working_dir)