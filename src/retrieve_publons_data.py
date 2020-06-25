# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Mai 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: A partir do arquivo com os ids da API do Publons, verifica se os dados do id USP já foram coletados, se sim, pula para o próximo id senão, faz a chamada para coletar as informações.
'''

import csv
import json
import time
from os import makedirs
from os.path import exists, join

import requests

from general import get_files


def main():
    print('Iniciando...')
    wait_time = [3, 5, 7, 9]
    i = 0
    s = requests.Session()

    with open('../config.json') as f:
            config = json.load(f)

    publons_info_path = config['publons_info']
    if not exists(publons_info_path):
        print('Nenhum dado a ser recuperado.')
        return 0

    publons_file = join(publons_info_path, 'publons_info_unique_filtered.csv')
    if exists(publons_file) == False:
        print('Nenhum dado a ser recuperado.')
        return 0

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

    # Procura dados recuperados previamente
    data_recovered_files = get_files(publons_data_path, 'json')
    data_recovered = []
    if data_recovered_files:
        for data_recovered_file in data_recovered_files:
            usp_id = data_recovered_file.split('_')[0]
            data_recovered.append(usp_id)
    print('Qtd. de dados recuperados previamente: ', len(data_recovered))

    # Procura dados analisados previamente com problema
    data_missing_file = join(publons_data_path, 'data_missing.txt')
    if exists(data_missing_file):
        with open(data_missing_file, 'r') as f:
            data_missing = f.read().split(',')
        if len(data_missing) == 1 and data_missing.pop() == '':
            data_missing = []
    else:
        data_missing = []
    print('Qtd. de dados com problema previamente: ', len(data_missing))

    count = 0
    with open(publons_file, 'r', newline='') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)
            if count < 2000:
                for row in csv_reader:
                    usp_id = row[0]
                    publons_id = row[4]

                    if usp_id in data_analysed:
                        continue
                    else:
                        print('Recuperando dados de: ', usp_id + '_' + publons_id, flush=True)

                    if i == 4:
                        i = 0
                    time.sleep(wait_time[i])
                    i = i + 1

                    url = 'https://publons.com/researcher/api/' + publons_id + '/metrics/individualStats/'
                    try:
                        response = s.get(url)
                    except requests.exceptions.ConnectionError:
                        time.sleep(60)
                        response = s.get(url)

                    count = count + 1
                    if response:
                        r = response.json()
                        if 'ready' in r and len(r.keys()) == 1:
                            print('Sem dados.')
                            if usp_id not in data_missing:
                                data_missing.append(usp_id)
                            with open(data_missing_file, 'w', newline='') as f:
                                print('Escrevendo arquivo sem resposta...')
                                f.write(','.join(data_missing))
                        else:
                            with open(join(publons_data_path, usp_id + '_' +       publons_id + '.json'), 'w', encoding='utf-8') as f:
                                json.dump(response.json(), f, ensure_ascii=False, indent=4)
                            print('Dado recuperado com sucesso.')
                    else:
                        print('Sem dados.')
                        if usp_id not in data_missing:
                            data_missing.append(usp_id)
                        with open(data_missing_file, 'w', newline='') as f:
                            print('Escrevendo arquivo sem resposta...')
                            f.write(','.join(data_missing))

                    if usp_id not in data_analysed:
                        data_analysed.append(usp_id)
                    # Escrevendo arquivo com dado recuperado
                    with open(data_analysed_file, 'w', newline='') as f:
                        f.write(','.join(data_analysed))
            else:
                print('Limite atingido. Por favor, execute esse sript novamente em 24 horas.')

    print('------')
    print('Requisitados: ', count)
    print('Qtd. de dados analisados: ', len(data_analysed))
    print('Qtd. de dados recuperados: ', len(data_analysed) - len(data_missing))
    print('Sem dados: ', len(data_missing))
    print('Fim')

if __name__ == '__main__':
    main()
