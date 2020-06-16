# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Recupera departamentos de cada unidade da USP.
'''

import json
import time
from os import makedirs
from os.path import exists, join

import requests

from general import get_files


def get_depts(units, path):
    s = requests.Session()
    wait_time = [3, 5, 7, 9]
    saved_units = units
    i = 0

    for unit in units:
        print('Recuperando dados de departamento da unidade: ', unit, flush=True)

        if i == 4:
            i = 0
        time.sleep(wait_time[i])
        i = i + 1

        url = 'https://uspdigital.usp.br/datausp/servicos/publico/listagem/departamentos/' + str(unit)
        try:
            response = s.get(url)
        except requests.exceptions.ConnectionError:
            time.sleep(60)
            response = s.get(url)

        with open(join(path,'deptos_unidade_' + str(unit) + '.json'), 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        saved_units.remove(unit)
    return saved_units

def main():
    all_units = [30,64,86,27,39,90,7,22,88,18,3,11,16,9,60,2,89,12,81,48,59,8,5,17,10,23,25,58,6,74,93,14,41,42,55,4,31,43,76,44,45,83,47,46,75,87,21,71,32,38,33,1]

    all_units.sort()

    with open('../config.json') as f:
        config = json.load(f)

    if not exists(config['depts']):
        makedirs(config['depts'])

    files = get_files(config['depts'], 'json')
    saved_units = []

    if len(files) > 0:
        for file in files:
            unit = file.split('_').pop()[:-5]
            if unit not in saved_units:
                saved_units.append(int(unit))
        saved_units.sort()
    else:
        print('Nenhum departamento recuperado previamente.')

    print('Iniciando...')
    units = list(set(all_units) - set(saved_units))
    while len(units) > 0:
        units = get_depts(units, config['depts'])
    else:
        print('Dados dos departamentos recuperados.')

if __name__ == '__main__':
    main()
