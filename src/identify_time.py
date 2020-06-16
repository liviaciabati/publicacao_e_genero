# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Jun 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Identificar o tempo de trabalho de pesquisadores da USP com base no portal de transparência. Adiciona também unidade e departamento USP aos dados Publons.

@url https://brasil.io/dataset/genero-nomes/nomes/?=format=csv
'''

import csv
import json
from os import makedirs
from os.path import exists, getsize, join

from general import remove_accent_mark


def main():
    print('Iniciando...')

    with open('../config.json') as f:
            config = json.load(f)

    publons_info_path = config['publons_info']
    if not exists(publons_info_path):
        print('Nenhum dado a ser recuperado.')
        return 0

    publons_info_gender = join(publons_info_path, 'publons_info_unique_filtered_gender.csv')
    if not exists(publons_info_gender) or getsize(publons_info_gender) == 0:
        print('Por favor, gere o arquivo publons com informação de gênero.')
        return 0

    time_worked_path = config['resources']
    time_worked_file = join(time_worked_path, 'USP.txt')
    if not exists(time_worked_file) or getsize(time_worked_file) == 0:
        print('Por favor, faça o download do arquivo no portal de transparência da USP.')

    print('Criando dicionário de tempo de trabalho.')
    time_worked = dict()
    with open(time_worked_file, 'r', newline='', encoding='latin-1') as f:
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)
        for row in csv_reader:
            name = remove_accent_mark((
                        row[0].lower().replace(' ','-')))
            time = row[9]
            time_worked[name] = time
    print('Dicionário criado. Quantidade de pesquisadores: ', len(time_worked))

    # Fazendo o match de nomes de pesquisador com o tempo de trabalho
    print('Fazendo o match de nomes de pesquisador com o tempo de trabalho.')
    with open(publons_info_gender, 'r', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        rows = []
        researchers = dict()
        for row in csv_reader:
            usp_id = row[0]
            usp_name = row[1]
            usp_unit = row[2]
            usp_dept = row[3]
            if usp_name in time_worked:
                row.append(time_worked[usp_name])
                researchers[usp_id] = {'time_worked': time_worked[usp_name], 'usp_unit': usp_unit, 'usp_dept': usp_dept}
            else:
                row.append('time_not_found')
            rows.append(row)

    # Escreve novo arquivo com informação de tempo de trabalho
    print('Novo arquivo criado com gênero e tempo de trabalho.')
    publons_info_gender_time = join(publons_info_path, 'publons_info_unique_filtered_gender_time.csv')
    with open(publons_info_gender_time, 'w', newline='') as f:
            csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
            csv_writer.writerow(['usp_id','usp_name','usp_unit','usp_dept','publons_id','publons_name','gender','time'])
            csv_writer.writerows(rows)

    # Verificação de existência dos dados Publons posteriores
    publons_results_path = config['publons_results']
    if not exists(publons_results_path):
        print('Por favor, garanta que os dados publons já foram recuperados.')
        return 0

    publons_results_gender = join(publons_results_path, 
                                    'results_publons_gender.csv')
    if not exists(publons_results_gender) or getsize(publons_results_gender) == 0:
        print('Por favor, garanta que os dados publons já foram recuperados e o gênero adicionado.')
        return 0

    # Atualizando resultados Publons com informação de tempo de trabalho
    with open(publons_results_gender, 'r', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        publons_data = []
        for row in csv_reader:
            usp_id = row[0]
            if usp_id in researchers:
                row.append(researchers[usp_id]['time_worked'])
                row.append(researchers[usp_id]['usp_unit'])
                row.append(researchers[usp_id]['usp_dept'])
                publons_data.append(row)

    print('Novo arquivo criado com dados Publons e informação de tempo de trabalho.')
    publons_results_gender_time = join(publons_results_path, 'results_publons_gender_time.csv')
    with open(publons_results_gender_time, 'w', newline='') as f:
            csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
            csv_writer.writerow(['usp_id','nr_wos_publication','citations','h_index','gender', 'time','usp_unit','usp_dept'])
            csv_writer.writerows(publons_data)

if __name__ == '__main__':
    main()
