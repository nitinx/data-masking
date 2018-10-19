# 03 May 2018 | Traverse File Delimited Library

"""Traverse File Library
Library that:
1. Masks delimited files - driven by column names
2. Masks delimited files - driven by column positions
"""

import csv
import logging
from mylibrary.mask import Mask

log = logging.getLogger(__name__)

Mask = Mask()


class FileDelimited:

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

    def mask_by_col_name(self, data, metadata_index, file_rec_count):
        """Mask delimited file - driven by column name (optimized)"""
        log.debug("mask_by_col_name() | <START>")

        # Read File | Data
        with open(self.filename, 'r', newline='') as file_read:
            rec_count = itr_count = 0

            # Check if file has header record
            snf = csv.Sniffer().has_header(file_read.read(100))
            log.info('Has Header: ' + str(snf))
            file_read.seek(0)

            reader = csv.DictReader(file_read, fieldnames=None, delimiter=data[metadata_index]['delimiter'],
                                    quoting=csv.QUOTE_ALL)
            col_names = reader.fieldnames

            # Write File | Masked Data
            with open(self.filename_masked, 'w', newline='') as file_write:
                writer = csv.DictWriter(file_write, fieldnames=col_names, delimiter=data[metadata_index]['delimiter'],
                                        quoting=csv.QUOTE_NONE)
                writer.writeheader()

                # Loop through each record
                for row_read in reader:
                    row_write = row_read

                    # Skip masking for trailer record
                    if ((data[metadata_index]['trailer_present'] == 'No') or
                            (data[metadata_index]['trailer_present'] == 'Yes' and rec_count < file_rec_count - 2)):

                        # Loop through masked columns
                        for mask_col in range(len(data[metadata_index]['masking']['columns'])):
                            itr_count += 1

                            itr_col_name = data[metadata_index]['masking']['columns'][mask_col]['name']
                            itr_col_type = data[metadata_index]['masking']['columns'][mask_col]['type']

                            # Mask column value
                            if itr_col_type == 'ShuffleDet':
                                row_write[itr_col_name] = Mask.shuffle_det(row_read[itr_col_name])
                            elif itr_col_type == 'Shuffle':
                                row_write[itr_col_name] = Mask.shuffle(row_read[itr_col_name])
                            elif itr_col_type == 'SubstitutionChar':
                                row_write[itr_col_name] = Mask.substitution_char(row_read[itr_col_name])
                            elif itr_col_type == 'SubstitutionCharDet':
                                row_write[itr_col_name] = Mask.substitution_char_det(row_read[itr_col_name])
                    else:
                        # Special handling for trailer record
                        col_names_trailer = []
                        row_write = {}

                        # Loop through trailer columns
                        for col in range(int(data[metadata_index]['trailer_column_count'])):
                            col_names_trailer.append(str(col))
                            row_write[col_names_trailer[col]] = row_read[col_names[col]]

                        # Reinitialize writer for trailer column names
                        writer = csv.DictWriter(file_write, fieldnames=col_names_trailer,
                                                delimiter=data[metadata_index]['delimiter'],
                                                quoting=csv.QUOTE_NONE, extrasaction='ignore')

                    log.debug(row_write)
                    writer.writerow(row_write)
                    rec_count += 1
                    if (rec_count == file_rec_count - 1) or ((rec_count % 10000) == 0):
                        log.info("# of Records Processed: " + str(rec_count))
                        log.info("# of Iterations: " + str(itr_count))

        log.debug("mask_by_col_name() | <END>")

    def mask_by_col_position(self, data, metadata_index, file_rec_count):
        """Mask delimited file - driven by column position"""
        log.debug("mask_by_col_position() | <START>")

        # Read File | Data
        with open(self.filename, 'r', newline='') as file_read:
            rec_count = itr_count = 0

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

                        # Loop through masked columns
                        for mask_col in range(len(data[metadata_index]['masking']['columns'])):
                            itr_count += 1
                            itr_col_type = data[metadata_index]['masking']['columns'][mask_col]['type']
                            itr_col_position = int(data[metadata_index]['masking']['columns'][mask_col]['position']) - 1

                            # Mask column values
                            if itr_col_type == 'Shuffle':
                                row_write[itr_col_position] = Mask.shuffle(row_read[itr_col_position])
                            elif itr_col_type == 'ShuffleDet':
                                row_write[itr_col_position] = Mask.shuffle_det(row_read[itr_col_position])
                            elif itr_col_type == 'SubstitutionChar':
                                row_write[itr_col_position] = Mask.substitution_char(row_read[itr_col_position])
                            elif itr_col_type == 'SubstitutionCharDet':
                                row_write[itr_col_position] = Mask.substitution_char_det(row_read[itr_col_position])

                    log.debug(row_write)
                    writer.writerow(row_write)
                    rec_count += 1
                    if (rec_count == file_rec_count - 1) or ((rec_count % 10000) == 0):
                        log.info("# of Records Processed: " + str(rec_count))
                        log.info("# of Iterations: " + str(itr_count))

        log.debug("mask_by_col_position() | <END>")
