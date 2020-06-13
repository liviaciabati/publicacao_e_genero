# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Gera novo arquivo com arquivos analisados, removendo os arquivos faltantes.

'''

import json
from os.path import join, exists

def main():
    print('Iniciando...')

    with open('../config.json') as f:
            config = json.load(f)

    publons_data_path = config['publons_data']
    if not exists(publons_data_path):
        makedirs(publons_data_path)

    # Procura dados analisados previamente
    data_analysed_file = join(publons_data_path, 'data_analysed.txt')
    if exists(data_analysed_file):
        with open(data_analysed_file, 'r') as f:
            data_analysed = f.read().split(',')
    else:
        data_analysed = []
    print('Qtd. de dados analisados previamente: ', len(data_analysed))

    # Procura dados analisados previamente com problema
    data_missing_file = join(publons_data_path, 'data_missing.txt')
    if exists(data_missing_file):
        with open(data_missing_file, 'r') as f:
            data_missing = f.read().split(',')
        if len(data_missing) == 1 and data_missing.pop() == '':
            print('Sem dados faltantes.')
            return 0
    else:
        print('Sem dados faltantes.')
        return 0
    print('Qtd. de dados com problema previamente: ', len(data_missing))

    for missing in data_missing:
        if missing in data_analysed:
            data_analysed.remove(missing)
        
    # Escrevendo arquivo com dado recuperado e excluindo missing
    data_analysed.reverse() # coloca os últimos arquivos primeiro
    with open(data_analysed_file, 'w', newline='') as f:
        f.write(','.join(set(data_analysed)))

    # Deletando arquivo de dados faltantes
    with open(data_missing_file, 'w', newline='') as f:
        f.write('')
    
    print('Qtd. de dados no novo arquivo: ', len(data_analysed))

if __name__ == '__main__':
    main()