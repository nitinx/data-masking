# 03 May 2018 | Traverse File Library

"""Traverse File Library
Library that:
"""

import csv
import logging
from mylibrary.mask import Mask

log = logging.getLogger(__name__)

Mask = Mask()


class Delimited:


    def read_write_file(self, data, file_index):
        """Reads data file and creates masked files"""
        log.debug("read_write_file() | <START>")

        # Read File | Data
        with open('sampledata.csv', 'r', newline='') as file_read:

            # Check if file has header record
            snf = csv.Sniffer().has_header(file_read.read(100))
            log.info('Has Header: ' + str(snf))
            file_read.seek(0)

            reader = csv.DictReader(file_read, fieldnames=None, delimiter=data[file_index]['delimiter'],
                                    quoting=csv.QUOTE_ALL)
            fieldnames = reader.fieldnames
            #print(fieldnames)

            # Write File | Masked Data
            with open('sampledata_masked.csv', 'w', newline='') as file_write:
                writer = csv.DictWriter(file_write, fieldnames=fieldnames, delimiter=data[file_index]['delimiter'],
                                        quoting=csv.QUOTE_NONE)
                writer.writeheader()

                for row_read in reader:
                    row_write = row_read
                    for field in range(len(fieldnames)):
                        for mask_field in range(len(data[file_index]['masking']['fields'])):
                            if fieldnames[field] == data[file_index]['masking']['fields'][mask_field]['name']:
                                if data[file_index]['masking']['fields'][mask_field]['type'] == 'Shuffle':
                                    row_write[fieldnames[field]] = Mask.shuffle(row_read[fieldnames[field]])
                                elif data[file_index]['masking']['fields'][mask_field]['type'] == 'SubstitutionChar':
                                    row_write[fieldnames[field]] = Mask.substitution_char(row_read[fieldnames[field]])

                    writer.writerow(row_write)
        log.debug("read_write_file() | <END>")
