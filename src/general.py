# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Funções genéricas
'''

from os import listdir
from os.path import isfile, join
from unicodedata import normalize


def get_files(my_path, file_type):
    file_names = [f for f in listdir(my_path)
                    if isfile(join(my_path, f))
                    and f.split('.').pop() == file_type]
    file_names.sort()
    return file_names

def remove_accent_mark(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')