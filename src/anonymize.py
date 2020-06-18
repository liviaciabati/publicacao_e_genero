# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Jun 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Anonimiza o dataset final obtido.

@see: Código adaptado de https://stackoverflow.com/questions/4618298/randomly-mix-lines-of-3-million-line-file
'''

import json
import random
from os.path import exists, getsize, join


def main():
    print('Iniciando...')

    with open('../config.json') as f:
            config = json.load(f)

    publons_results_path = config['publons_results']
    publons_results_gender_time = join(publons_results_path, 'results_publons_gender_time.csv')
    if not exists(publons_results_gender_time) or getsize(publons_results_gender_time) == 0:
            print('Arquivo inexistente.')
            return 0

    publons_anonymized = join(publons_results_path, 'results_publons_gender_time_anonymized.csv')
    print('Anonimza e escreve novo arquivo')
    with open(publons_results_gender_time,'r') as source:
        next(source)
        data = [(random.random(), line) for line in source]
    data.sort()

    with open(publons_anonymized,'w') as target:
        target.write('wos_publication,citations,citations_per_item,citations_per_year,h_index,gender,time,usp_unit,usp_dept')
        target.write('\n')
        for _, line in data:
            anonymized_line = line.split(',')[1:]
            target.write(','.join(anonymized_line))

if __name__ == '__main__':
    main()
