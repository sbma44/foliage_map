import sys
import json
from shapely.geometry import mapping, shape
from shapely.ops import cascaded_union
from fiona import collection

BUFFER_SIZE = 0.1

if __name__ == '__main__':

    with collection(sys.argv[1], 'r') as shp:

        output_shapes = []
        for s in shp:
            output_shapes.append(shape(s['geometry']).buffer(BUFFER_SIZE).buffer(-1 * BUFFER_SIZE).buffer(0.5 * BUFFER_SIZE))

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

