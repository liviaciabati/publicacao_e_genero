# -*- coding: utf-8 -*-
'''
Created on Dec 2019
Updated on Apr 2020

@authors: Livia Ciabati, Ariane Sasso

@objective: Remove ids com nomes que não batem (usp e publons).
'''

import json
import csv

from os.path import join, exists

def main():
    # Define IDs a serem removidos
    usp_ids = [87922,43141,74970,70472,3388141,35614,47569,41890,1075420,2091563,96338,33546]

    with open('../config.json') as f:
        config = json.load(f)

    path = config['publons_info']
    if not exists(path):
        print('Nenhum dado a ser filtrado.')
        return 0

    publons_file = join(path, 'publons_info_unique.csv')
    if exists(publons_file) == False:
        print('Nenhum dado a ser filtrado.')
        return 0

    publons_info_unique_filtered = join(path, 'publons_info_unique_filtered.csv')
    with open(publons_info_unique_filtered, 'w', newline='') as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
        csv_writer.writerow(['usp_id', 'usp_name', 'publons_id', 'publons_name'])

    # Removendo ids
    filtered_info = []
    with open(publons_file, 'r', newline='') as  f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        total_rows = 0
        rows_mantained = 0
        for row in csv_reader:
            if int(row[0]) not in usp_ids:
                filtered_info.append(row)
                rows_mantained = rows_mantained + 1
            total_rows = total_rows + 1

    with open(publons_info_unique_filtered, 'a', newline='') as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,          escapechar='\\')
        csv_writer.writerows(filtered_info)

    print('Qtd IDs iniciais: ', total_rows)
    print('Qts IDs para remover: ', len(usp_ids))
    print('Qtd IDs remanescentes: ', rows_mantained)

if __name__ == '__main__':
    main()