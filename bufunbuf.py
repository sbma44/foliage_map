import sys
import json
from shapely.geometry import mapping, shape
from shapely.ops import cascaded_union
from fiona import collection

BUFFER_SIZE = 0.2

if __name__ == '__main__':

    # find max area -- this will correspond to blank images that have been converted to full rects
    max_area = 0
    with collection(sys.argv[1], 'r') as shp:
        for s in shp:
            max_area = max(max_area, float(shape(s['geometry']).area))

    with collection(sys.argv[1], 'r') as shp:
        output_shapes = []
        for s in shp:
            with open('areas.csv', 'a') as f2:
                f2.write(sys.argv[1])
                f2.write(',')
                f2.write(str(shape(s['geometry']).area))
                f2.write("\n")                

            shape_obj = shape(s['geometry'])
            
            # leave out objects that fill the screen
            # if shape_obj.area < 0.95 * max_area:
            if True:
                output_shapes.append(shape_obj.buffer(BUFFER_SIZE).buffer(-1 * BUFFER_SIZE).buffer(0.5 * BUFFER_SIZE))

        # empty? skip writing the file
        if len(output_shapes):
            
            merged = cascaded_union(output_shapes)

            features = {
                "type": "FeatureCollection", 
                "features": [ {
                    'type': 'Feature',
                    'properties': { 'name': 'buffered object'},
                    'geometry': mapping(merged)
                } ]
            }

            if sys.argv[2].strip() == '-':
                print json.dumps(features, indent=2)
            else:
                with open(sys.argv[2], 'w') as out:    
                    json.dump(features, out)                    

