# -*- coding: utf-8 -*-
"""
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Recupera informações do arquivo Publons de cada pesquisador.
"""

import requests
import csv
import time
import json

from os import makedirs
from os.path import join, exists

from general import get_files

def main():
    print('Iniciando...')

    with open('../config.json') as f:
            config = json.load(f)

    publons_data_path = config['publons_data']
    if not exists(publons_data_path):
        print('Nenhum dado a ser recuperado.')
        return 0

    files = get_files(publons_data_path, 'json')

    if len(files) == 0:
        print('Nenhum dado a ser recuperado.')
        return 0

    publons_results_path = config['publons_results']
    if not exists(publons_results_path):
        makedirs(publons_results_path)

    # Procura dados recuperados previamente
    data_analysed_file = join(publons_results_path, 'data_publons_analysed.txt')
    if exists(data_analysed_file):
        with open(data_analysed_file, 'r') as f:
            data_analysed = f.read().split(',')
        print("Qtd. de dados recuperados previamente: ", len(data_analysed))
    else:
        data_analysed = []

    for file in files:
        publons_file = join(publons_data_path, file)
        information = json.load(publons_file)

if __name__ == '__main__':
    main()