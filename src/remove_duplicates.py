# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Recupera professores de cada departamento da USP
'''

import json
import csv

from os import makedirs
from os.path import join, exists

from general import get_files

def main():
    with open('../config.json') as f:
        config = json.load(f)

    if not exists(config['output']):
        print('Nenhum dado a ser deduplicados.')
        return 0

    publons_file = join(config['output'], 'ids_publons.csv')
    if exists(publons_file) == False:
        print('Nenhum dado a ser deduplicados.')
        return 0

    with open(join(config['output'], 'ids_publons_unique.csv'), 'w', newline='') as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
        csv_writer.writerow(['num_usp', 'id_publon'])

    # Adptado de:
    lines_seen = set()
    with open(publons_file, 'r', newline='') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)
            count_rows = 0
            for row in csv_reader:
                count_rows = count_rows + 1
                line = ','.join(row)
                if line not in lines_seen: # não é duplicado
                    with open(join(config['output'], 'ids_publons_unique.csv'), 'a', newline='') as f:
                        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
                        csv_writer.writerow(line.split(','))
                    lines_seen.add(line)
    print('Nr. de ids: ', count_rows)
    print('Nr. de ids deduplicados: ', len(lines_seen))

if __name__ == '__main__':
    main()