# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Jun 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Identifica o gênero de pesquisadores com base no CENSO de 2010.

@url https://brasil.io/dataset/genero-nomes/nomes/?=format=csv
'''

import csv
import json
from os import makedirs
from os.path import exists, getsize, join

import requests

from general import remove_accent_mark


def main():
    print('Iniciando...')

    with open('../config.json') as f:
            config = json.load(f)

    publons_info_path = config['publons_info']
    if not exists(publons_info_path):
        print('Nenhum dado a ser recuperado.')
        return 0

    publons_info = join(publons_info_path, 'publons_info_unique_filtered.csv')
    if not exists(publons_info) or getsize(publons_info == 0):
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
        for row in csv_reader:
            name = remove_accent_mark((
                        row[0].lower().replace(' ','-')))
            gender = row[2]
            names[name] = gender
    print('Dicionário criado. Quanditade de nomes: ', len(names))

    # Fazendo o match de nomes de pesquisador com o gênero
    print('Fazendo o match de nomes de pesquisador com o gênero.')
    with open(publons_info, 'r', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        rows = []
        researchers = dict()
        for row in csv_reader:
            usp_id = row[0]
            researcher_name = row[1].split('-')[0]
            if researcher_name in names:
                row.append(names[researcher_name])
                researchers[usp_id] = names[researcher_name]
            else:
                row.append('gender_not_found')
            rows.append(row)

    # Escreve novo arquivo com informação de gênero
    print('Novo arquivo criado com nome e gênero.')
    publons_info_with_gender = join(publons_info_path, 'publons_info_unique_filtered_gender.csv')
    with open(publons_info_with_gender, 'w', newline='') as f:
            csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
            csv_writer.writerow(['usp_id','usp_name','usp_unit','usp_dept', 'publons_id','publons_name','gender'])
            csv_writer.writerows(rows)

    # Verificação de existência dos dados posteriores
    publons_results_path = config['publons_results']
    if not exists(publons_results_path):
        print('Por favor, garanta que os dados publons já foram recuperados.')
        return 0

    publons_results = join(publons_results_path, 'results_publons.csv')
    if not exists(publons_results):
        print('Por favor, garanta que os dados publons já foram recuperados.')
        return 0

    # Atualizando resultados Publons com gênero
    with open(publons_results, 'r', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        publons_data = []
        for row in csv_reader:
            usp_id = row[0].split('-')[0]
            if usp_id in researchers:
                row.append(researchers[usp_id])
                publons_data.append(row)

    print('Novo arquivo criado com dados Publons e gênero.')
    publons_results_with_gender = join(publons_results_path, 'results_publons_gender.csv')
    with open(publons_results_with_gender, 'w', newline='') as f:
            csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
            csv_writer.writerow(['usp_id','wos_publications','citations','citations_per_item','citations_per_year','h_index','gender'])
            csv_writer.writerows(publons_data)

if __name__ == '__main__':
    main()
