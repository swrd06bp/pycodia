import os
import json
from pycodya import config

def get_relative_path(root_path, file_path):
        root_array = os.path.normpath(root_path).split(os.sep)
        file_array = os.path.normpath(file_path).split(os.sep)
        relative_array = [p for p in file_array if p not in root_array]
        relative_path = os.path.join(*relative_array)
        return relative_path

def create_unitestfiles(data):
    # create folder if not exists
    if not os.path.isdir(config.DIR_GENERATED_TESTS):
        os.makedirs(config.DIR_GENERATED_TESTS)

    # create files

    list_files = []
    for d in data:
        if d['fileName'] not in list_files:
            list_files.append(d['fileName'])


    for file in list_files:
        data_file = []
        for d in data:
            if d['fileName'] == file:
                
                data_file.append({
                    'fileName': d['fileName'],
                    'filePath': d['filePath'],
                    'funcName': d['funcName'],
                    'dataInput': d['dataInput'],
                    'dataOutput': d['dataOutput']
                })
        path_file = os.path.join(
            config.DIR_GENERATED_TESTS,
            file + '.json'
        )
        with open(path_file, 'w') as f:
            json.dump(data_file, f)
        print("Created file: {}".format(path_file))    

        
