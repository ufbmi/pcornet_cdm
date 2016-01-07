#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jiang Bian (bianjiang@ufl.edu)
v0.01: 

'''

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

import sys, csv, re, os

def get_data_type(rdbms_data_type):

    mapping = {
        'text': 'VARCHAR',
        'number': 'NUMERIC',
        'date': 'DATETIME',
        'x': '50'
    }

    m = re.match(r"\w+\s(\w+)((\((.*?)\))*)", rdbms_data_type)
    if (m):
        datatype = m.group(1).strip().lower()
        length = m.group(4).strip().lower() if m.group(4) else 0
        
        return mapping[datatype] if 'date' == datatype else '%s(%s)'%(mapping[datatype], mapping[length] if length in mapping else int(length))
    else:
        logger.error('failed to convert! %s'%rdbms_data_type)
        sys.exit(-1)

def pcornet_cdm(fields_csv, relational_csv, constratins_csv):
    tables = {}
    constraints = {}
    relationals = {}

    with open(fields_csv, 'r',newline="",encoding='latin-1') as ff, open(relational_csv, 'r',newline="",encoding='latin-1') as rf, open(constratins_csv, 'r',newline="",encoding='latin-1') as cf:
        f_reader = csv.DictReader(ff, delimiter=',')

        for row in f_reader:
            table_name = row['TABLE_NAME'].strip()
            if (table_name not in tables):
                tables[table_name] = {}

            tables[table_name][row['FIELD_NAME'].strip()] = {
                'RDBMS_DATA_TYPE': get_data_type(row['RDBMS_DATA_TYPE'].strip()),
                'CDM_ORDER': int(row['CDM_ORDER'].strip())
            } 

        c_reader = csv.DictReader(cf, delimiter=',')

        for row in c_reader:

            table_name = row['TABLE_NAME'].strip()
            field_names = [f.strip() for f in row['FIELD_NAME'].strip().split(',')]

            for field_name in field_names:

                if (table_name not in constraints):
                    constraints[table_name] = {}
                    
                if (field_name not in constraints[table_name]):
                    constraints[table_name][field_name] = []

                constraints[table_name][field_name] += [c.strip() for c in row['CONSTRAINT'].strip().split(',')]

        r_reader = csv.DictReader(rf, delimiter=',')

        for row in r_reader:
            table_name = row['TABLE_NAME'].strip()
            if (table_name not in relationals):
                relationals[table_name] = {}
            relationals[table_name][row['RELATION'].strip()] = row['RELATIONAL INTEGRITY DETAILS'].strip()

    return tables, constraints, relationals

current = os.path.dirname(os.path.abspath(__file__))

tables, constraints, relationals = pcornet_cdm(os.path.join(current, 'CDM.v3.Fields.csv'), os.path.join(current, 'CDM.v3.Relational.csv'), os.path.join(current, 'CDM.v3.Constraints.csv'))
 
if __name__ == "__main__":

    logger.info(sys.version)
    tables, constraints, relationals = pcornet_cdm('CDM.v3.Fields.csv', 'CDM.v3.Relational.csv', 'CDM.v3.Constraints.csv')




