#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jiang Bian (bianjiang@ufl.edu)
v0.01: 
    - unique constraint is not enforced;
    - FK is not enforced;
    - required is ignored (as it's equivalent to  not null )
'''
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

import sys, csv, re


def bootstrap_cdm_tables(tables, constraints, relationals):

    sql = ''
    for table_name in tables:
        table = tables[table_name]
        fields = dict(table.items())
        sorted_field_keys = sorted(fields, key=lambda x:fields[x]['CDM_ORDER'])


        sql += "\nIF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[%s]') AND type in (N'U'))\nDROP TABLE [dbo].[%s]\nGO\n"%(table_name, table_name)
        sql += "CREATE TABLE [dbo].[%s](\n"%(table_name)
        for field_key in sorted_field_keys:
            sql += '\t[%s] %s'%(field_key, table[field_key]['RDBMS_DATA_TYPE'])

            #just add null or not null to the field, required is ignored (as it's equivalent to  not null )
            if (table_name in constraints and field_key in constraints[table_name]):
                if ('null' in constraints[table_name][field_key]):
                    sql += ' NULL'
                elif('not null' in constraints[table_name][field_key]):
                    sql += ' NOT NULL'
                else:
                    pass # don't care

            sql += ',\n'

        sql += '\t[UPDATED] DATETIME NOT NULL DEFAULT GETDATE(),\n'
        sql += '\t[SOURCE] VARCHAR(50) NOT NULL,\n'
        pks = []
        if (table_name in relationals):
            if ('PK' in relationals[table_name]):
                pks.append(relationals[table_name]['PK'])
            if ('Composite Key' in relationals[table_name]):
                pks += [pk.strip() for pk in relationals[table_name]['Composite Key'].split('+')]
            sql += "PRIMARY KEY CLUSTERED\n(\n%s\n)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]) ON [PRIMARY]\nGO\nSET ANSI_PADDING OFF\nGO\n"%(',\n'.join(['\t[%s] ASC'%pk for pk in pks]))
    return sql
 
if __name__ == "__main__":

    import cdm.pcornet_cdm
    logger.info(sys.version)
    bootstrap_sql = bootstrap_cdm_tables(cdm.pcornet_cdm.tables, cdm.pcornet_cdm.constraints, cdm.pcornet_cdm.relationals)
    logger.info(bootstrap_sql)


