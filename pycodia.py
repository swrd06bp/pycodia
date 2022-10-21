import os
import json

import config

class Codia(object):
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
        self.is_testing = False
        self.root_dir = os.path.dirname(os.path.abspath(__file__)) + '/'

        if not os.path.isdir(config.DIR_GENERATED_TESTS):
            os.makedirs(config.DIR_GENERATED_TESTS)

    def _set_testing(self, is_testing):
        """
        Setter for is_testing

        Input
        :is_testing: true if we are running the tests
        """
        self.is_testing = is_testing


    def _get_stored_output(self, file_path, function_name, data_input):
        """
        
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

        for d in stored_data:
            if d['filePath'] == file_path.replace(self.root_dir, '') \
               and d['funcName'] == function_name \
               and d['dataInput'] == list(data_input):
               return d['dataOutput'] 
        return 

    def _store_test(self, file_path, function_name, data_input, data_output, is_mocked=False):
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

        new_data = {
            'filePath': file_path.replace(self.root_dir, ''),    
            'funcName': function_name,
            'dataInput': list(data_input),
            'dataOutput': data_output,
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

        if not flag:
            stored_data.append(new_data)

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
                return self._get_stored_output(
                    func.__globals__['__file__'],
                    func.__name__,
                    args,
                    )

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

