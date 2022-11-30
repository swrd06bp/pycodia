import os
import json
import requests

from pycodya.helpers import tools
from pycodya import config
from pycodya.codya_api import CodyaApi

class Codya(object):
    """
    Class that creates some testing environment for decoration on the local environment
    Only needs to be initated once for the entire project 
    """

    def __init__(self, token=None):
        """
        Initialise the class

        Input
        :token: (uuid) unique to the customer and project
        """
        self.token = token
        self.api = CodyaApi(self.token)
        self.is_testing = False
        self.ROOT_DIR = os.path.abspath(os.curdir)

        if not os.path.isdir(config.DIR_GENERATED_TESTS):
            os.makedirs(config.DIR_GENERATED_TESTS)


    def _set_testing(self, is_testing):
        """
        Setter for is_testing

        Input
        :is_testing: true if we are running the tests
        """
        self.is_testing = is_testing

    def _send_data(self, new_data):
        """
        Send the input and output of the function while the function is runnning
        to codya api server
        
        Inputs
        :new_data: (Obj) new data object with the following keys 
            :file_path: (string) absolute file path of the file which contains the function to be tested
            :function_name: name of the function to be tested
            :data_input: args given to the function to be tested
            :data_output: output of the data to be tested stored in the test files
        """
        self.api._send_data(new_data) 

        
        



    def _get_stored_output(self, file_path, function_name, data_input):
        """
        Get all the stored output from the test files stored while the functions were running

        Inputs
        :file_path: (string) absolute file path of the file which contains the function to be tested
        :function_name: name of the function to be tested
        :data_input: args given to the function to be tested

        Output
        :data_output: output of the data to be tested stored in the test files
        """
        file_name = file_path.split('/')[-1]
        output_file = '{}/{}.json'.format(
            config.DIR_GENERATED_TESTS,
            file_name
        )
        
        if not os.path.isfile(output_file):
            return

        with open(output_file) as fr:
            stored_data = json.load(fr)
        
        relative_path = tools.get_relative_path(self.ROOT_DIR, file_path)

        for d in stored_data:
            if d['filePath'] == relative_path \
               and d['funcName'] == function_name \
               and d['dataInput'] == list(data_input):
                try:
                    return list(d['dataOutput'])
                except:
                    return list([d['dataOnput']])
        return 

    def _store_test(self, file_path, function_name, data_input, data_output, is_mocked=False):
        """
        Store the input and output of the function while the function is runnning
        
        Inputs
        :file_path: (string) absolute file path of the file which contains the function to be tested
        :function_name: name of the function to be tested
        :data_input: args given to the function to be tested
        :data_output: output of the data to be tested stored in the test files
        :is_mocked: check if the function is mocked
        """
        file_name = file_path.split('/')[-1]
        output_file = '{}/{}.json'.format(
            config.DIR_GENERATED_TESTS,
            file_name
        )
        
        if os.path.isfile(output_file):
            with open(output_file) as fr:
                stored_data = json.load(fr)
        else:
            stored_data = []
        
        relative_path = tools.get_relative_path(self.ROOT_DIR, file_path)
        
        try:
            list_data_output = list(data_output)
        except:
            list_data_output = list([data_output])
        
        new_data = {
            'fileName': file_name,    
            'filePath': relative_path, 
            'funcName': function_name,
            'dataInput': list(data_input),
            'dataOutput': list_data_output,
        }
                
        flag = False
        for d in stored_data:
            if not is_mocked and d == new_data:
                flag = True
                break
            if is_mocked \
                and d['filePath'] == new_data['filePath'] \
                and d['funcName'] == new_data['funcName'] \
                and d['dataInput'] == new_data['dataInput']:
                flag = True
                break

        # if the data has not been found, store it
        if not flag:
            stored_data.append(new_data)
            # if there is a token send the data
            if self.token:
                self._send_data(new_data)


        fw = open(output_file, 'w')
        json.dump(stored_data, fw)
        fw.close()

    def function_tester(self, func):
        """
        Function decorator to test some predictable function

        Input
        :func: function to be tested

        Return
        :output: output of the function
        """
        def inner(*args, **kwargs):
            # get the result 
            result = func(*args, **kwargs)

            # store the function attributes for later
            if not self.is_testing:
                self._store_test(
                    func.__globals__['__file__'],
                    func.__name__,
                    args,
                    result,
                    is_mocked=False,
                )
            return result
        return inner
    
    def function_mock(self, func):
        """
        Function decorator to test some unpredictable function.
        During the test time, the function will be mocked

        Input
        :func: function to be tested

        Return
        :output: output of the function
        """
        def inner(*args, **kwargs):
            # 
            if self.is_testing:
                result = self._get_stored_output(
                    func.__globals__['__file__'],
                    func.__name__,
                    args,
                    )
                if len(result) == 1: return result[0]
                else: return tupple(result)

            # get the result 
            result = func(*args, **kwargs)
            
            # store the function attributes for later
            self._store_test(
                func.__globals__['__file__'],
                func.__name__,
                args,
                result,
                is_mocked=True,
            )
            return result 
        return inner


    def class_function_test(self, func):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            print("I can decorate any class", self.token, func.__name__, 'arguments', args[0].__dict__, 'result', result)
            return result
        return inner


