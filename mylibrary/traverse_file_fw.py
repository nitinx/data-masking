# 03 May 2018 | Traverse File FixedWidth Library

"""Traverse File FixedWidth Library
Library that:
1. Masks fixed-width files by column position
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
        """Converts file layout from fixed width --> delimited"""
        log.debug("convert_to_dl() | <START>")

        # Read File | Data
        with open(self.filename, 'r', newline='') as file_read:
            rec_count = itr_count = 0

            # Loop through each record
            for row in file_read:
                row_list = []

                # Skip masking for header/trailer record(s)
                if ((data[metadata_index]['header_present'] == 'Yes' and rec_count == 0) or
                        (data[metadata_index]['trailer_present'] == 'Yes' and rec_count == file_rec_count - 1)):
                    row_list.append(row[:])

                else:
                    # If first column to be masked does not start at position 0
                    if int(data[metadata_index]['masking']['columns'][0]['position_start']) > 0:
                        row_list.append(row[0:int(data[metadata_index]['masking']['columns'][0]['position_start']) - 1])
                        print(row_list)

                    # Loop through record and create a list of columns
                    for columns in range(len(data[metadata_index]['masking']['columns'])):
                        print(columns)
                        itr_count += 1
                        itr_col_type = data[metadata_index]['masking']['columns'][columns]['type']
                        itr_col_pos_start = int(data[metadata_index]['masking']['columns'][columns]
                                                ['position_start']) - 1
                        itr_col_pos_end = int(data[metadata_index]['masking']['columns'][columns]['position_end']) - 1

                        # Mask column values
                        if itr_col_type == 'Shuffle':
                            row_list.append(Mask.shuffle(row[itr_col_pos_start:itr_col_pos_end]))
                        elif itr_col_type == 'ShuffleDet':
                            row_list.append(Mask.shuffle_det(row[itr_col_pos_start:itr_col_pos_end]))
                        elif itr_col_type == 'SubstitutionChar':
                            row_list.append(Mask.substitution_char(row[itr_col_pos_start:itr_col_pos_end]))
                        elif itr_col_type == 'SubstitutionCharDet':
                            row_list.append(Mask.substitution_char_det(row[itr_col_pos_start:itr_col_pos_end]))
                        print(row_list)

                        if columns < len(data[metadata_index]['masking']['columns']) - 1:
                            itr_col_nxt_pos_start = int(data[metadata_index]['masking']['columns'][columns + 1]
                                                        ['position_start']) - 1
                            if itr_col_nxt_pos_start - itr_col_pos_end > 1:
                                row_list.append(row[itr_col_pos_end:itr_col_nxt_pos_start])
                                print(row_list)
                        else:
                            if len(row[itr_col_pos_end:]) > 0:
                                row_list.append(row[itr_col_pos_end:])
                                print(row_list)

                        # ON ADDITION of below, iteration is misbehaving
                        #row = ''.join(row_list)
                        #print(row)

                rec_count += 1
                if (rec_count == file_rec_count - 1) or ((rec_count % 10000) == 0):
                    log.info("# of Records Processed: " + str(rec_count))
                    log.info("# of Iterations: " + str(itr_count))

        log.debug("convert_to_dl() | <END>")
