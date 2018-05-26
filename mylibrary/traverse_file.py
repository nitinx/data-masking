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
        log.info('# of Records' + str(i + 1))
        return i + 1

    def read_write_file(self, data, metadata_index, file_rec_count):
        """Reads data file and creates masked files"""
        log.debug("read_write_file() | <START>")

        # Read File | Data
        with open(self.filename, 'r', newline='') as file_read:
            rec_count = 0

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

                for row_read in reader:
                    row_write = row_read
                    for col in range(len(col_names)):
                        for mask_col in range(len(data[metadata_index]['masking']['columns'])):
                            if col_names[col] == data[metadata_index]['masking']['columns'][mask_col]['name']:
                                if data[metadata_index]['masking']['columns'][mask_col]['type'] == 'Shuffle':
                                    row_write[col_names[col]] = Mask.shuffle(row_read[col_names[col]])
                                elif data[metadata_index]['masking']['columns'][mask_col]['type'] == 'SubstitutionChar':
                                    row_write[col_names[col]] = Mask.substitution_char(row_read[col_names[col]])

                    writer.writerow(row_write)
                    rec_count += 1
                    if (rec_count == file_rec_count - 1) or ((rec_count % 10000) == 0):
                        log.info("Records Processed: " + str(rec_count))
        log.debug("read_write_file() | <END>")
