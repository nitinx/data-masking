# 03 May 2018 | Traverse File Library

"""Traverse File Library
Library that:
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

    def mask_data(self, data, metadata_index, file_rec_count):
        """Reads data file and creates masked files"""
        log.debug("mask_data() | <START>")

        # Read File | Data
        with open(self.filename, 'r', newline='') as file_read:
            rec_count = 0

            # Check if file has header record
            '''snf = csv.Sniffer().has_header(file_read.read(100))
            log.info('Has Header: ' + str(snf))
            file_read.seek(0)'''

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

                        # Loop through each column
                        for col in range(len(col_names)):

                            # Loop through masked columns
                            for mask_col in range(len(data[metadata_index]['masking']['columns'])):
                                if col_names[col] == data[metadata_index]['masking']['columns'][mask_col]['name']:
                                    if data[metadata_index]['masking']['columns'][mask_col]['type'] == 'Shuffle':
                                        row_write[col_names[col]] = Mask.shuffle(row_read[col_names[col]])
                                    elif data[metadata_index]['masking']['columns'][mask_col]['type'] == \
                                            'SubstitutionChar':
                                        row_write[col_names[col]] = Mask.substitution_char(row_read[col_names[col]])
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

        log.debug("mask_data() | <END>")
