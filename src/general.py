from os import listdir
from os.path import isfile, join

def get_files(my_path, file_type):
    file_names = [f for f in listdir(my_path)
                    if isfile(join(my_path, f))
                    and f.split('.').pop() == file_type]
    file_names.sort()
    return file_names