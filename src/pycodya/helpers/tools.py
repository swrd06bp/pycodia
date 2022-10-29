import os

def get_relative_path(root_path, file_path):
        root_array = os.path.normpath(root_path).split(os.sep)
        file_array = os.path.normpath(file_path).split(os.sep)
        relative_array = [p for p in file_array if p not in root_array]
        relative_path = os.path.join(*relative_array)
        return relative_path
