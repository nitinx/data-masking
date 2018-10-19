# 03 May 2018 | Traverse File FixedWidth Library

"""Traverse File FixedWidth Library
Library that:
1. Masks fixed-width files column positions
"""

import csv
import logging
from mylibrary.mask import Mask

log = logging.getLogger(__name__)

Mask = Mask()


class FileFixedWidth:

    def __init__(self, filename):
        self.filename = filename
        filename_list = self.filename.split('.')
        self.filename_masked = filename_list[0] + '_masked.' + filename_list[1]

    def record_count(self):
        with open(self.filename) as f:
            for i, l in enumerate(f):
                pass
        log.info('# of Records: ' + str(i + 1))
        return i + 1

    def convert_to_dl(self, data, metadata_index, file_rec_count):
        """Converts file layout from delimited --> fixed width"""
        log.debug("convert_to_dl() | <START>")

        # Read File | Data
        with open(self.filename, 'r', newline='') as file_read:
            rec_count = 0
            row_list = []

            for row in file_read:
                print(row)

                row_list = row[0:int(data[metadata_index]['masking']['columns'][0]['position_start'])]
                print(row_list)

                #for columns in range(len(data[metadata_index]['masking']['columns']) + 2):
                    #print(str(columns) + ': ' + row[2:5])



    def mask_data(self, data, metadata_index, file_rec_count):
        """Masks file data by column position"""
        log.debug("mask_data() | <START>")

        # Read File | Data
        with open(self.filename, 'r', newline='') as file_read:
            rec_count = 0

            reader = csv.reader(file_read, delimiter=data[metadata_index]['delimiter'])

            # Write File | Masked Data
            with open(self.filename_masked, 'w', newline='') as file_write:
                writer = csv.writer(file_write, delimiter=data[metadata_index]['delimiter'])

                # Loop through each record
                for row_read in reader:
                    row_write = row_read

                    # Mask Detail Records
                    '''if ((data[metadata_index]['trailer_present'] == 'No') or
                            (data[metadata_index]['trailer_present'] == 'Yes' and rec_count < file_rec_count - 1)):'''

                    # Skip masking for header/trailer record(s)
                    if ((data[metadata_index]['header_present'] == 'Yes' and rec_count == 0) or
                            (data[metadata_index]['trailer_present'] == 'Yes' and rec_count == file_rec_count - 1)):
                        if data[metadata_index]['header_present'] == 'Yes' and rec_count == 0:
                            rec_type = 'header'
                        else:
                            rec_type = 'trailer'

                        log.info('Processing ' + str.upper(rec_type) + ' Record...')
                        row_write = []

                        # Loop through trailer columns
                        for col in range(int(data[metadata_index][rec_type + '_column_count'])):
                            row_write.append(row_read[col])

                        # Reinitialize writer for header column names
                        writer = csv.writer(file_write, delimiter=data[metadata_index]['delimiter'],
                                            quoting=csv.QUOTE_NONE)

                    else:

                        # Loop through each column
                        for col in range(len(row_read)):

                            # Loop through masked columns
                            for mask_col in range(len(data[metadata_index]['masking']['columns'])):
                                if (col + 1) == int(data[metadata_index]['masking']['columns'][mask_col]['position']):
                                    if data[metadata_index]['masking']['columns'][mask_col]['type'] == 'Shuffle':
                                        row_write[col] = Mask.shuffle(row_read[col])
                                    if data[metadata_index]['masking']['columns'][mask_col]['type'] == 'ShuffleDet':
                                        row_write[col] = Mask.shuffle_det(row_read[col])
                                    elif data[metadata_index]['masking']['columns'][mask_col]['type'] == \
                                            'SubstitutionChar':
                                        row_write[col] = Mask.substitution_char(row_read[col])
                                    elif data[metadata_index]['masking']['columns'][mask_col]['type'] == \
                                            'SubstitutionCharDet':
                                        row_write[col] = Mask.substitution_char_det(row_read[col])

                    log.debug(row_write)
                    writer.writerow(row_write)
                    rec_count += 1
                    if (rec_count == file_rec_count - 1) or ((rec_count % 10000) == 0):
                        log.info("# of Records Processed: " + str(rec_count))

        log.debug("mask_data() | <END>")
