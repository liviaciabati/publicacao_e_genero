# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Identificar o gênero de pesquisadores com base no CENSO de 2010.

@url https://brasil.io/dataset/genero-nomes/nomes/?=format=csv
'''

import requests
import csv
import json

from os import makedirs
from os.path import join, exists, getsize

from general import remove_accent_mark

def main():
    print('Iniciando...')

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

    gender_path = config['resources']
    if not exists(gender_path):
        print('Criando diretórios de recursos.')
        makedirs(gender_path)

    gender_file = join(gender_path, 'genero-nomes.csv')
    gender_file_url = 'https://brasil.io/dataset/genero-nomes/nomes/?=format%3Dcsv&format=csv'
    
    if not exists(gender_file) or getsize(gender_file) == 0:
        with requests.Session() as s:
            download = s.get(gender_file_url)
            decoded_content = download.content.decode('utf-8')
            with open(gender_file, 'w') as f:
                f.write(decoded_content)
        print('Arquivo salvo com sucesso.')

    print('Criando dicionário de nomes')
    names = dict()
    with open(gender_file, 'r', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        count = 0
        for row in csv_reader:
            count = count + 1
            name = remove_accent_mark((
                        row[0].lower().replace(' ','-')))
            gender = row[2]
            names[name] = gender
    print('Dicionário criado. Quanditade de nomes: ', len(names))
    
    # Fazendo o match de nomes de pesquisador com o gênero
    print('Fazendo o match de nomes de pesquisador com o gênero.')
    with open(publons_file, 'r', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        rows = []
        for row in csv_reader:
            researcher_name = row[1].split('-')[0]
            if researcher_name in names:
                row.append(names[researcher_name])
            else:
                row.append('not_found')
            rows.append(row)

    # Escreve novo arquivo com informação de gênero
    print('Novo arquivo criado.')
    publons_file_with_gender = join(publons_info_path, 'publons_info_unique_filtered_gender.csv')
    with open(publons_file_with_gender, 'w', newline='') as f:
            csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
            csv_writer.writerow(['usp_id', 'usp_name', 'publons_id', 'publons_name','gender'])
            csv_writer.writerows(rows)

if __name__ == '__main__':
    main()