import os
import copy
import yaml

TM2SOURCE = './foliage.tm2source/data.yml'

if __name__ == '__main__':
    
    data_yml = None    
    with open(TM2SOURCE, 'r') as f:
        data_yml = yaml.load(f)

    source_template = yaml.load("""Layer: 
  - id: mylayer
    Datasource: 
      file: /Users/tomlee/mapbox/code/python/foliage_map/json/09082014_lc-5-done.json
      layer: OGRGeoJSON
      type: ogr
    description: this is the description
    fields: 
      name: name field value goes here
    properties: 
      "buffer-size": 8
    srs: +proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs""")

    sources = []

    for filename in os.listdir('./json'):   
        filename = os.getcwd() + '/json/' + filename

        basename = os.path.basename(filename).replace('-done.json', '')   

        new_source = copy.deepcopy(source_template['Layer'][0])    
        new_source['id'] = basename
        new_source['Datasource']['file'] = filename
        # new_source['Datasource']['layer'] = basename
        
        new_source['fields']['name'] = basename
        new_source['fields']['month'] = basename[0:2]
        new_source['fields']['day'] = basename[2:4]
        new_source['fields']['year'] = basename[4:8]
        
        sources.append(new_source)

    data_yml['Layer'] = sources

    # print yaml.dump(data_yml)

    with open(TM2SOURCE, 'w') as f:
        yaml.dump(data_yml, f)

