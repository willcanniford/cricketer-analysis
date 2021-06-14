import os
import yaml
import pandas as pd 

innings_lookup = {
    '1st innings': 'first_innings',
    '2nd innings': 'second_innings',
    '3rd innings': 'third_innings',
    '4th innings': 'fourth_innings'
}


def load_yaml_file(filepath):
    with open(filepath, 'r') as stream:
        try:
            raw_data = yaml.safe_load(stream)
            meta = raw_data['meta']
            info = raw_data['info']
            innings = raw_data['innings']
            innings_processed = {}
            innings_processed['n_innings'] = len(innings)

            for inning in innings: 
                original_key = list(inning.keys())[0]
                key = innings_lookup[original_key]
                print(original_key, key)
                print(inning[original_key]['team'])
                innings_processed[key] = inning[original_key]['team']
            
            return innings_processed

        except yaml.YAMLError as exc:
            print(exc)


#print(meta, info, innings_processed['n_innings'])
#print(innings[0]['1st innings'].keys())
data = load_yaml_file("files/64071.yaml")
print(data)