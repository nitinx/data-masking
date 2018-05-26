# 26 May 2018 | Traverse Table Library

"""Traverse Table Library
Library that:
"""

import csv
import logging
import cx_Oracle
from mylibrary.mask import Mask
from mylibrary.db_oracle import OracleClient

log = logging.getLogger(__name__)

DB = OracleClient()
db_conn = DB.db_login()
db_cur_one = db_conn.cursor()
db_cur_two = db_conn.cursor()

Mask = Mask()


class Oracle:

    def __init__(self, table, schema):
        self.table = str.upper(table)
        self.schema = str.upper(schema)
        self.filename_masked = str.upper(schema) + '.' + str.upper(table) + '_masked.dat'
        self.col_attr_file = self.schema + '.' + self.table + '.dat'

    def get_column_count(self):
        """Retrieve Column Count"""

        db_cur_one.execute("""SELECT count(*)
                                FROM all_tab_columns
                               WHERE owner = :schema
                                 AND table_name = :table_name""", schema=self.schema, table_name=self.table)

        for values in db_cur_one:
            col_cnt = values[0]
            log.info('# of Columns: ' + str(col_cnt))
        return 0

    def get_column_attributes(self):
        """Retrieve Column Attributes"""

        db_cur_one.execute("""SELECT column_id, column_name, data_type
                                FROM all_tab_columns
                               WHERE owner = :schema
                                 AND table_name = :table_name
                            ORDER BY column_id""", schema=self.schema, table_name=self.table)

        with open(self.col_attr_file, 'w') as file:
            col_names = ['column_id', 'column_name', 'data_type']
            writer = csv.DictWriter(file, fieldnames=col_names, lineterminator='\n', delimiter='|')
            writer.writeheader()

            for values in db_cur_one:
                writer.writerow({'column_id': values[0], 'column_name': values[1], 'data_type': values[2]})
                log.debug(str(values[0]) + ' ' + values[1] + ' ' + values[2])
        return 0

    def get_record_count(self):
        """Returns Table Record Count"""
        query = 'SELECT count(*) from {schema}.{table}'.format(schema=self.schema, table=self.table)
        db_cur_one.execute(query)

        for values in db_cur_one:
            rec_cnt = values[0]

        log.info('# of Records: ' + str(rec_cnt))
        return rec_cnt

    def mask_data(self, data, metadata_index, col_count, table_rec_count):
        """Reads table and creates masked files"""
        log.debug("mask_data() | <START>")

        # Retrieve Column Attributes
        with open(self.col_attr_file, 'r') as file:
            reader = csv.DictReader(file, fieldnames=None, delimiter='|', quoting=csv.QUOTE_ALL)
            #col_names_attr = reader.fieldnames
            #print(col_names_attr)

            # Compile Header of Masked File
            col_names_write = []
            for row_read in reader:
                col_names_write.append(row_read['column_name'])

        # Write File | Masked Data
        with open(self.filename_masked, 'w', newline='') as file_write:
            rec_count = 0
            writer = csv.DictWriter(file_write, fieldnames=col_names_write, delimiter='|', quoting=csv.QUOTE_ALL)
            writer.writeheader()

            query = 'SELECT * FROM {schema}.{table}'.format(schema=self.schema, table=self.table)
            db_cur_one.execute(query)
            row_write = {}

            for row_read in db_cur_one:
                for col_read in range(len(col_names_write)):
                    col_value = str.strip(str(row_read[col_read]))
                    row_write[col_names_write[col_read]] = col_value

                    for col_mask in range(len(data[metadata_index]['masking']['columns'])):
                        if col_names_write[col_read] == \
                                str.strip(str(data[metadata_index]['masking']['columns'][col_mask]['name'])):
                            if data[metadata_index]['masking']['columns'][col_mask]['type'] == 'Shuffle':
                                row_write[col_names_write[col_read]] = Mask.shuffle(col_value)
                            elif data[metadata_index]['masking']['columns'][col_mask]['type'] == 'SubstitutionChar':
                                row_write[col_names_write[col_read]] = Mask.substitution_char(col_value)

                log.debug(row_write)
                writer.writerow(row_write)
                rec_count += 1
                if (rec_count == table_rec_count - 1) or ((rec_count % 10000) == 0):
                    log.info("Records Processed: " + str(rec_count))

        log.debug("mask_data() | <END>")
