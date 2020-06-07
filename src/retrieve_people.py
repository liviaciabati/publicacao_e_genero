# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Recupera professores de cada departamento da USP
'''

import requests
import json
import time
import csv

from os import makedirs
from os.path import join, exists

from general import get_files

def main():
    url_professors = 'https://uspdigital.usp.br/datausp/servicos/publico/citacoes/docentes/'

    headings = ['google',
                'scopus',
                'web_of_science',
                'link_google',
                'link_scopus',
                'link_web_of_science',
                'cod_person_g',
                'cod_person_s',
                'cod_person_w',
                'name'
    ]

    wait_time = [3, 5, 7]
    s = requests.Session()

    with open('../config.json') as f:
        config = json.load(f)

    if not exists(config['depts']):
        print('Nenhum dado a ser recuperado.')
        return 0

    if not exists(config['people']):
        makedirs(config['people'])

    files = get_files(config['depts'], 'json')

    if len(files) == 0:
        print('Nenhum dado a ser recuperado.')
        return 0

    # Procura unidades recuperadas previamente
    units_recovered_file = join(config['people'], 'units_recovered.txt')
    if exists(units_recovered_file):
        with open(units_recovered_file, 'r') as f:
            units = f.read().split(',')
    else:
        units = []

    print('Iniciando...')
    for file in files:
        unit = file.split('_').pop()[:-5]
        file_path = join(config['depts'], file)

        if unit in units:
            print('Unidade recuperada previamente: ', unit, flush=True)
            continue
        else:
            print('Recuperando dados da unidade: ', unit, flush=True)

        # Lê arquivo de departamentos
        with open(file_path, 'r', encoding='utf-8') as f:
            if f.read(2) != '[]' and f.read(2) != '':
                f.seek(0)
                data = json.load(f)
            else:
                print('Sem dados da unidade: ', unit, flush=True)
                units.append(unit)

                with open(units_recovered_file, 'w', newline='') as f:
                    print('Escrevendo arquivo com unidade recuperada...')
                    f.write(','.join(units))

                continue

        # Recupera dados de pesquisadores por unidade
        if len(data) > 0:
            for dept in data:
                print('Departamento: ', dept['codset'], flush=True)

                url_g = url_professors+ str(unit) +'/'+ str(dept['codset']) +'/1998/2018/G'
                url_s = url_professors+ str(unit) +'/'+ str(dept['codset']) +'/1998/2018/S'
                url_w = url_professors+ str(unit) +'/'+ str(dept['codset']) +'/1998/2018/W'

                google = []
                scopus = []
                web_of_science = []
                name = []

                link_google = []
                link_scopus = []
                link_web_of_science = []

                cod_person_g = []
                cod_person_s = []
                cod_person_w = []

                time.sleep(wait_time[0])
                try:
                    response = s.get(url_g)
                except requests.exceptions.ConnectionError:
                    time.sleep(60)
                    response = s.get(url_g)
                lista_g = response.json()
                if len(lista_g) > 0:
                    for person in lista_g:
                        cod_person_g.append(person['codpes'])

                        google.append(
                            person['idfpesfte']
                            if person ['idfpesfte'] != None else '')

                        link_google.append(
                            'http://scholar.google.com/citations?user='+ person['idfpesfte'] +'&hl=en'
                            if person['idfpesfte'] != None else '')

                time.sleep(wait_time[1])
                try:
                    response = s.get(url_s)
                except requests.exceptions.ConnectionError:
                    time.sleep(60)
                    response = s.get(url_s)
                lista_s = response.json()
                if len(lista_s) > 0:
                    for person in lista_s:
                        cod_person_s.append(person['codpes'])

                        scopus.append(person['idfpesfte']
                        if person['idfpesfte'] != None
                        else '')

                        link_scopus.append('https://www.scopus.com/authid/detail.url?authorId=' + person['idfpesfte']
                        if person['idfpesfte'] != None else '')

                time.sleep(wait_time[2])
                try:
                    response = s.get(url_w)
                except requests.exceptions.ConnectionError:
                    time.sleep(60)
                    response = s.get(url_w)
                lista_w = response.json()
                if len(lista_w) > 0:
                    for person in lista_w:
                        cod_person_w.append(person['codpes'])

                        web_of_science.append(person['idfpesfte']
                        if person['idfpesfte'] != None
                        else '')

                        link_web_of_science.append('http://www.researcherid.com/rid/' + person['idfpesfte']
                        if person['idfpesfte'] != None else '')

                        name.append(person['nompes'])

                information = zip(google,
                                    scopus,
                                    web_of_science,
                                    link_google,
                                    link_scopus,
                                    link_web_of_science,
                                    cod_person_g,
                                    cod_person_s,
                                    cod_person_w,
                                    name)

                with open(join(config['people'], str(unit) +'_'+ str(dept['codset']) + '.csv'), 'w', newline='') as f:
                    csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
                    csv_writer.writerow(headings)
                    if information:
                        csv_writer.writerows(information)

        print('Dados recuperados da unidade: ', unit, flush=True)
        units.append(unit)

        with open(units_recovered_file, 'w', newline='') as f:
            print('Escrevendo arquivo com unidade recuperada...')
            f.write(','.join(units))

    print('Fim')

if __name__ == '__main__':
    main()