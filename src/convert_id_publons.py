# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: A partir de arquivos com as urls do "web of science", converte o "researcher indentifier" para o identificador da API publons e salva o resultado em um arquivo
'''

import requests
import csv
import time
import json

from bs4 import BeautifulSoup
from os import makedirs
from os.path import join, exists

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

    if not exists(config['output']):
        makedirs(config['output'])

    # Procura departamentos recuperados previamente
    depts_recovered_file = join(config['output'], 'depts_recovered.txt')
    if exists(depts_recovered_file):
        with open(depts_recovered_file, 'r') as f:
            depts = f.read().split(',')
        print("Departamentos recuperados previamente: ", len(depts))
    else:
        depts = []

    publons_file = join(config['output'], 'ids_publons.csv')
    if exists(publons_file) == False:
        with open(join(config['output'], 'ids_publons.csv'), 'w', newline='') as f:
            csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
            csv_writer.writerow(['num_usp', 'id_publon'])

    new_ids = []
    i = 0
    for file in files:
        dept = file[:-4]
        new_ids = []

        if dept in depts:
            print('Departamento recuperado previamente: ', dept, flush=True)
            continue
        else:
            print('Recuperando dados do departamento: ', dept, flush=True)

        with open(join(config['people'], file), 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                url_wos = row[5]
                # O elemento 5 da row (linha) contém a url do web of science, que precisa ser transformada em id da API publon
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
                    # Pega o id pra refazer a url
                    num_usp = row[7]
                    name = remove_accent_mark((row[9].lower().replace(' ','-')))
                    if page.find('meta', attrs={'property':'og:url'}) != None:
                        new_id = page.find('meta',
                        attrs={'property':'og:url'})['content'].split('/')[4]

                        new_ids.append({'num_usp': num_usp,
                                        'id_publons': new_id,
                                        'name': name})
                    else:
                        new_ids.append({'num_usp': num_usp,
                                        'id_publons': 'missing_id',
                                        'name': name})

        if new_ids:
            with open(join(config['output'], 'ids_publons.csv'), 'a', newline='') as f:
                csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
                for new_id in new_ids:
                    csv_writer.writerow([new_id['num_usp'], new_id['id_publons'], new_id['name']])

        print('Dados recuperados do departamento: ', dept, flush=True)
        depts.append(dept)

        with open(join(config['output'], 'depts_recovered.txt'), 'w', newline='') as f:
            print('Escrevendo arquivo com departamento recuperado...')
            f.write(','.join(depts))

    print('Departamentos recuperados: ', len(depts))
    print('Fim')

if __name__ == '__main__':
    main()