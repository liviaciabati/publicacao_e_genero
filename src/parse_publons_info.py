# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Remove ids publons duplicados
'''

import json
import csv

from os import makedirs
from os.path import join, exists

from general import get_files

def remove_duplicates_and_missing(path, publons_file):
    parsed_file = join(path, 'publons_info_unique.csv')
    with open(parsed_file, 'w', newline='') as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
        csv_writer.writerow(['usp_id', 'usp_name', 'publons_id', 'publons_name'])

    file_duplicates = join(path, 'publons_info_duplicates.csv')
    with open(file_duplicates, 'w', newline='') as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
        csv_writer.writerow(['usp_id', 'usp_name', 'publons_id', 'publons_name'])

    # Adptado de:
    lines_seen = set()
    duplicates = []
    with open(publons_file, 'r', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        count_rows = 0
        missing = 0
        for row in csv_reader:
            count_rows = count_rows + 1
            line = ','.join(row)
            if line not in lines_seen: # não é duplicado
                if row[2] != 'missing_id':
                    with open(parsed_file, 'a', newline='') as f:
                        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
                        csv_writer.writerow(line.split(','))
                    lines_seen.add(line)
                else:
                    missing = missing + 1
            else:
                with open(file_duplicates, 'a', newline='') as f:
                    csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
                    csv_writer.writerow(line.split(','))
                duplicates.append(line)

    print('Nr. de ids: ', count_rows)
    print('Nr. de ids exclusivos e not missing: ', len(lines_seen))
    print('Nr. de ids duplicados: ', len(duplicates))
    print('Nr. de ids missing: ', missing)
    print('Nr. de ids mais de uma vez duplicados: ', len(duplicates) - len(set(duplicates)))
    return parsed_file

def verify_names(path, file):
    file_not_matching = join(path, 'publons_info_not_matching.csv')

    with open(file_not_matching, 'w', newline='') as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
        csv_writer.writerow(['usp_id', 'usp_name', 'publons_id', 'publons_name'])

    count = 0
    with open(file, 'r', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            usp_name = row[1].replace('junior','jr')
            publons_name = row[3].replace('junior','jr')

            usp_first_name = usp_name.split('-')[0]
            usp_last_name = usp_name.split('-').pop()
            usp_second_last_name = usp_name.split('-')[-2:][0]

            publons_first_name = publons_name.split('-')[0]
            publons_last_name = publons_name.split('-').pop()
            publons_second_last_name = publons_name.split('-')[-2:][0]

            if (usp_first_name == publons_first_name) and ((usp_last_name == publons_last_name) or (usp_last_name == publons_second_last_name)  or (usp_second_last_name == publons_last_name)):
                continue
            else:
                count = count + 1
                with open(file_not_matching, 'a', newline='') as f:
                    csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
                    csv_writer.writerow(row)
    print('Nomes diferentes: ', count)

def main():
    with open('../config.json') as f:
        config = json.load(f)

    path = config['output']
    if not exists(path):
        print('Nenhum dado a ser deduplicados.')
        return 0

    publons_file = join(path, 'publons_info.csv')
    if exists(publons_file) == False:
        print('Nenhum dado a ser deduplicados.')
        return 0

    parsed_file = remove_duplicates_and_missing(path, publons_file)
    verify_names(path, parsed_file)

if __name__ == '__main__':
    main()