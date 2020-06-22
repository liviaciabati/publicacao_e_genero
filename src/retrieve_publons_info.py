# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Mai 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: A partir de arquivos com as urls do 'web of science', converte o 'researcher indentifier' para o identificador da API Publons e salva o resultado em um arquivo.
'''

import csv
import json
import time
from os import makedirs
from os.path import exists, join

import requests
from bs4 import BeautifulSoup

from general import get_files, remove_accent_mark


def main():
    print('Iniciando...')
    wait_time = [3, 5, 7, 9]
    s = requests.Session()

    with open('../config.json') as f:
            config = json.load(f)

    if not exists(config['people']):
        print('Nenhum dado a ser recuperado.')
        return 0

    files = get_files(config['people'], 'csv')

    if len(files) == 0:
        print('Nenhum dado a ser recuperado.')
        return 0

    if not exists(config['publons_info']):
        makedirs(config['publons_info'])

    # Procura departamentos recuperados previamente
    depts_recovered_file = join(config['publons_info'], 'depts_recovered.txt')
    if exists(depts_recovered_file):
        with open(depts_recovered_file, 'r') as f:
            depts = f.read().split(',')
        print('Departamentos recuperados previamente: ', len(depts))
    else:
        depts = []

    publons_file = join(config['publons_info'], 'publons_info.csv')
    if exists(publons_file) == False:
        print('Novo arquivo criado.')
        with open(publons_file, 'w', newline='') as f:
            csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
            csv_writer.writerow(['usp_id', 'usp_name', 'usp_unit', 'usp_dept','publons_id', 'publons_name'])

    i = 0
    for file in files:
        file_name = file.split('_')
        unit = file_name[0]
        dept = file_name[1][:-4]
        unit_dept = unit + '_' + dept
        researchers_info = []

        if unit_dept in depts:
            print('Departamento recuperado previamente: ', unit_dept, flush=True)
            continue
        else:
            print('Recuperando dados do departamento: ', unit_dept, flush=True)

        with open(join(config['people'], file), 'r', newline='', encoding='latin-1') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                # O elemento 5 da row (linha) contém a url do web of science,que é usada para obtenção do id da API do Publons
                url_wos = row[5]
                # Pega o id para refazer a url
                usp_id = row[7]
                usp_name = remove_accent_mark((
                    row[9].lower().replace(' ','-')))
                if url_wos != '':
                    if i == 4:
                        i = 0
                        wait_time = [3, 5, 7, 9]
                        time.sleep(wait_time[i])
                        i = i + 1
                    try:
                        content = s.get(url_wos).text
                    except requests.exceptions.ConnectionError:
                        time.sleep(60)
                        content = s.get(url_wos).text
                    page = BeautifulSoup(content, 'lxml')

                    if page.find('meta', attrs={'property':'og:url'}) != None:
                        publons_id = page.find('meta',
                        attrs={'property':'og:url'})['content'].split('/')[4]

                        publons_name = page.find('meta', attrs={'property':'og:url'})['content'].split('/')[5]

                        researchers_info.append({'usp_id': usp_id,
                                        'usp_name': usp_name,
                                        'usp_unit': unit,
                                        'usp_dept': dept,
                                        'publons_id': publons_id,
                                        'publons_name': publons_name})
                    else:
                        researchers_info.append({'usp_id': usp_id,
                                        'usp_name': usp_name,
                                        'usp_unit': unit,
                                        'usp_dept': dept,
                                        'publons_id': 'missing_id',
                                        'publons_name': ''})
                else:
                    researchers_info.append({'usp_id': usp_id,
                                        'usp_name': usp_name,
                                        'usp_unit': unit,
                                        'usp_dept': dept,
                                        'publons_id': 'missing_id',
                                        'publons_name': ''})

        if researchers_info:
            with open(publons_file, 'a', newline='') as f:
                csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
                for researcher_info in researchers_info:
                    csv_writer.writerow([researcher_info['usp_id'], researcher_info['usp_name'], researcher_info['usp_unit'], researcher_info['usp_dept'], researcher_info['publons_id'], researcher_info['publons_name']])

        print('Dados recuperados do departamento: ', unit_dept, flush=True)
        depts.append(unit_dept)

        with open(depts_recovered_file, 'w', newline='') as f:
            print('Escrevendo arquivo com departamento recuperado...')
            f.write(','.join(depts))

    print('Departamentos recuperados: ', len(depts))
    print('Fim')

if __name__ == '__main__':
    main()
