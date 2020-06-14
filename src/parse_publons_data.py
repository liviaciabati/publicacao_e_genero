# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Recupera informações do arquivo Publons de cada pesquisador.
'''

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

    # Verifica se os dados estão disponíveis
    publons_data_path = config['publons_data']
    if not exists(publons_data_path):
        print('Nenhum dado a ser processado.')
        return 0

    files = get_files(publons_data_path, 'json')
    if len(files) == 0:
        print('Nenhum dado a ser processado.')
        return 0

    # Verifica se o path dos resultados foi criado
    publons_results_path = config['publons_results']
    if not exists(publons_results_path):
        makedirs(publons_results_path)

    # Verifica dados recuperados previamente
    publons_result_file = join(publons_results_path, 'results_publons' + '.csv')
    heading = ['usp_id','nr_wos_publication','citations','h_index']
    data_analysed = set()
    if not exists(publons_result_file):
        with open(publons_result_file, 'w', newline='') as f:
            csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
            csv_writer.writerow(heading)
    else:
        with open(publons_result_file, 'r', newline='') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                data_analysed.add(','.join(row))
        print('Qtd. de dados recuperados previamente: ', len(data_analysed))

    print('Processando dados')
    for file in files:
        publons_file = join(publons_data_path, file)
        usp_id = file.split('_')[0]

        # Lê arquivo de departamentos
        with open(publons_file, 'r', encoding='utf-8') as f:
            if f.read(2) != '[]' and f.read(2) != '':
                f.seek(0)
                data = json.load(f)
            else:
                print('Sem dados de usp_id: ', usp_id, flush=True)
                continue

            if 'numPublicationsInWos' not in data:
                data['numPublicationsInWos'] = ''
            if 'timesCited' not in data:
                data['timesCited'] = ''
            if 'hIndex' not in data:
                data['hIndex'] = ''

            information = ','.join([usp_id, str(data['numPublicationsInWos']), 
                                    str(data['timesCited']), str(data['hIndex'])])
            if information not in data_analysed:
                print('Dados salvos com sucesso.')
                with open(publons_result_file, 'a', newline='') as f:
                    csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
                    csv_writer.writerow([usp_id, data['numPublicationsInWos'], data['timesCited'], data['hIndex']])
        
    print('Nro de ids processados: ', len(files))

if __name__ == '__main__':
    main()