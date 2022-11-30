import os
import sys
import json
import time

from pycodya import config

# Add the current path
sys.path.append(os.getcwd())

def import_name(modulename, name):
    """
    Import a named object from a module in the context of this function
   
    Inputs
    :modulename: file you need to import
    :name: name of the function or class that needs to be imported

    Return
    :module: class, function or variables of the file that was imported
    """
    try:
        module = __import__(modulename, globals(), locals(), [name])
        return vars(module)[name]
    except ImportError as error:
        print(error)
        return None


def get_list_files():
    """
    Read list of test files generated from the test

    Return
    :list_files: paths of the list of files 
    """
    if not os.path.isdir(config.DIR_GENERATED_TESTS):
        return []

    list_files = os.listdir(config.DIR_GENERATED_TESTS) 
    return [l for l in list_files if l.endswith('.json')]

def read_file(file_name):
    """
    Extract the data out of the one file

    Input
    :file_name: name of the json file

    Return
    :json_data: json data from the file
    """
    json_data = json.load(open('{}/{}'.format(
        config.DIR_GENERATED_TESTS, 
        file_name
     )))
    return json_data                      



def test_file_functions(file_name, json_data):
    """
    Run all the tests of all the functions for one file

    Input
    :file_name: name of the stored json file 
    :json_data: data for the json file 
    """
    print('\nRunning tests in this file {}'.format(file_name.replace('.json', '')))

    for data in json_data:
        # Extract the name of the module
        module_name = data['filePath'].split('.')[0].replace('/', '.')
        
        # Get the function to be tested
        test_function = import_name(module_name, data['funcName'])
        
        # Make sure that the class CodyaTest is set to True
        file_module = import_name(module_name, config.PYCODYA_VAR_NAME)
        file_module._set_testing(True)

        # Run the test for that function
        input_function = data['dataInput']
        results = test_function(*input_function)

        if len(data['dataOutput']) == 1: data_output = data['dataOutput'][0]
        else: data_output = tuple(data['dataOutput'])

        # Analyse the results
        if results == data_output:
            print('\033[1m file: \033[0m {} - \033[1m function: \033[0m {} - \033[92m test OK \033[0m'
                .format(module_name, data['funcName']))
        else:
            raise AssertionError('\033[91m test FAIL \033[0m {} = {}'.format(results, data))
            

def run_tests():
    """
    Run all the tests from the data stored in the json files
    """
    # Start time to measure how long it takes to run the tests
    start_time = time.time()

    # Get the list of stored files
    list_files = get_list_files()

    if not len(list_files):
        print("No tests stored yet, please see the documentation to run tests")
    else:
        # Run the test for all the files
        for f in list_files:
            json_data = read_file(f)                      
            test_file_functions(f, json_data)

        print("\n\nThe tests took\033[1m {} \033[0m seconds to run".format(time.time() - start_time))



