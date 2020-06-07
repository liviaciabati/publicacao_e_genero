# -*- coding: utf-8 -*-
"""
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: A partir do arquivo com os ids da API do publons, verifica se os dados do num usp ja foram coletados, se sim, pula para o proximo senao, faz a chamada para coletar as informaçoes.
"""

import requests
import csv
import time
import json

from os import makedirs
from os.path import join, exists

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

    # Procura dados recuperados previamente
    data_recovered_file = join(config['publons_data'], 'data_analysed.txt')
    if exists(data_recovered_file):
        with open(data_recovered_file, 'r') as f:
            data_analysed = f.read().split(',')
        print("Qtd. de dados recuperados previamente: ", len(data_analysed))
    else:
        data_analysed = []

    with open(publons_file, 'r', newline='') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)
            no_data_recovered = 0
            for row in csv_reader:
                usp_id = row[0]
                publons_id = row[2]

                if usp_id in data_analysed:
                    print('Dado recuperado previamente: ', usp_id, flush=True)
                    continue
                else:
                    print('Recuperando dados de: ', usp_id, flush=True)

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

                if response:
                    with open(join(publons_data_path, publons_id + '.json'), 'w', encoding='utf-8') as f:
                        json.dump(response.json(), f, ensure_ascii=False, indent=4)
                else:
                    no_data_recovered = no_data_recovered + 1

                print('Dados analisados de: ', usp_id, flush=True)
                data_analysed.append(usp_id)

                with open(data_recovered_file, 'w', newline='') as f:
                    print('Escrevendo arquivo com dado recuperado...')
                    f.write(','.join(data_analysed))

    print('Qtd. de dados analisados: ', len(data_analysed))
    print('Qtd. de dados recuperados: ', len(data_analysed) - no_data_recovered)
    print('Sem dados: ', no_data_recovered)
    print('Fim')

if __name__ == '__main__':
    main()