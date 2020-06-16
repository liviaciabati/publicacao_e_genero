# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Remove ids publons duplicados e faltantes (missing_id).
'''

import csv
import json
from os import makedirs
from os.path import exists, join

from general import get_files


def remove_duplicates_and_missing(path, publons_file):
    parsed_file = join(path, 'publons_info_unique.csv')
    with open(parsed_file, 'w', newline='') as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
        csv_writer.writerow(['usp_id', 'usp_name', 'usp_unit',
                                        'usp_dept', 'publons_id', 'publons_name'])

    file_duplicates = join(path, 'publons_info_duplicates.csv')
    with open(file_duplicates, 'w', newline='') as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
        csv_writer.writerow(['usp_id', 'usp_name', 'usp_unit',
                                        'usp_dept', 'publons_id', 'publons_name'])

    ids_seen = set()
    duplicates = []
    with open(publons_file, 'r', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        count_rows = 0
        missing = 0
        for row in csv_reader:
            count_rows = count_rows + 1
            usp_id = row[0]
            if usp_id not in ids_seen: # não é duplicado
                publons_id = row[4]
                if publons_id != 'missing_id':
                    with open(parsed_file, 'a', newline='') as f:
                        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE, escapechar='\\')
                        csv_writer.writerow(row)
                    ids_seen.add(usp_id)
                else:
                    missing = missing + 1
            else:
                with open(file_duplicates, 'a', newline='') as f:
                    csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE, escapechar='\\')
                    csv_writer.writerow(row)
                duplicates.append(usp_id)

    print('Nr. de ids totais: ', count_rows)
    print('Nr. de ids exclusivos e not missing: ', len(ids_seen))
    print('Nr. de ids duplicados: ', len(duplicates))
    print('Nr. de ids missing: ', missing)
    print('EXTRA')
    print('Nr. de ids mais de uma vez duplicados: ', len(duplicates) - len(set(duplicates)))
    return parsed_file

def verify_names(path, file):
    file_not_matching = join(path, 'publons_info_not_matching.csv')

    with open(file_not_matching, 'w', newline='') as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
        csv_writer.writerow(['usp_id', 'usp_name', 'usp_unit',
                            'usp_dept', 'publons_id', 'publons_name'])

    count = 0
    with open(file, 'r', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            usp_name = row[1].replace('junior','jr')
            publons_name = row[5].replace('junior','jr')

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

    path = config['publons_info']
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
