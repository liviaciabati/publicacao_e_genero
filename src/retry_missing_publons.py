# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Gera novo arquivo com arquivos analisados, removendo os arquivos faltantes.

'''

import json
from os.path import join, exists

from general import get_files

def main():
    print('Iniciando...')

    with open('../config.json') as f:
            config = json.load(f)

    publons_data_path = config['publons_data']
    if not exists(publons_data_path):
        makedirs(publons_data_path)

    # Procura dados recuperados previamente
    data_recovered_files = get_files(publons_data_path, 'json')
    data_recovered = []
    if data_recovered_files:
        for data_recovered_file in data_recovered_files:
            usp_id = data_recovered_file.split('_')[0]
            data_recovered.append(usp_id)
    print('Qtd. de dados recuperados previamente: ', len(data_recovered))
        
    # Escrevendo arquivo com dados recuperados
    data_analysed_file = join(publons_data_path, 'data_analysed.txt')
    with open(data_analysed_file, 'w', newline='') as f:
        f.write(','.join(set(data_recovered)))

    # Deletando arquivo de dados faltantes
    data_missing_file = join(publons_data_path, 'data_missing.txt')
    with open(data_missing_file, 'w', newline='') as f:
        f.write('')
    
    print('Qtd. de dados no novo arquivo: ', len(data_recovered))

if __name__ == '__main__':
    main()