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

    '''def mask_data_by_col_name(self, data, metadata_index, file_rec_count):
        """Masks file data by column name"""
        log.debug("mask_data_by_col_name() | <START>")

        # Read File | Data
        with open(self.filename, 'r', newline='') as file_read:
            rec_count = itr_count = masked_col_position = 0

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
                        for col_mask in range(len(data[metadata_index]['masking']['columns'])):

                            itr_count += 1

                            col_mask_name = data[metadata_index]['masking']['columns'][col_mask]['name']
                            col_mask_type = data[metadata_index]['masking']['columns'][col_mask]['type']

                            # Mask column value
                            if col_mask_type == 'ShuffleDet':
                                row_write[col_mask_name] = Mask.shuffle_det(row_read[col_mask_name])
                            elif col_mask_type == 'Shuffle':
                                row_write[col_mask_name] = Mask.shuffle(row_read[col_mask_name])
                            elif col_mask_type == 'SubstitutionChar':
                                row_write[col_mask_name] = Mask.substitution_char(row_read[col_mask_name])
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

        log.debug("mask_data_by_col_name() | <END>")'''

    def mask_data_by_col_name(self, data, metadata_index, file_rec_count):
        """Masks file data by column name"""
        log.debug("mask_data_by_col_name() | <START>")

        # Read File | Data
        with open(self.filename, 'r', newline='') as file_read:
            rec_count = itr_count = masked_col_position = 0

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

                            # Loop through each column
                            for col in range(masked_col_position, len(col_names)):
                                itr_count += 1
                                if col_names[col] == data[metadata_index]['masking']['columns'][mask_col]['name']:

                                    # Track position of masked columns sequentially for optimization
                                    masked_col_position = col

                                    # Mask column value
                                    if data[metadata_index]['masking']['columns'][mask_col]['type'] == 'ShuffleDet':
                                        row_write[col_names[col]] = Mask.shuffle_det(row_read[col_names[col]])
                                    elif data[metadata_index]['masking']['columns'][mask_col]['type'] == 'Shuffle':
                                        row_write[col_names[col]] = Mask.shuffle(row_read[col_names[col]])
                                    elif data[metadata_index]['masking']['columns'][mask_col]['type'] == \
                                            'SubstitutionChar':
                                        row_write[col_names[col]] = Mask.substitution_char(row_read[col_names[col]])
                                    elif data[metadata_index]['masking']['columns'][mask_col]['type'] == \
                                            'SubstitutionCharDet':
                                        row_write[col_names[col]] = Mask.substitution_char_det(row_read[col_names[col]])
                                    #break
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

        log.debug("mask_data_by_col_name() | <END>")

    def mask_data_by_col_position(self, data, metadata_index, file_rec_count):
        """Masks file data by column position"""
        log.debug("mask_data_by_col_position() | <START>")

        # Read File | Data
        with open(self.filename, 'r', newline='') as file_read:
            rec_count = itr_count = masked_col_position = 0

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

                            # Loop through each column
                            for col in range(masked_col_position, len(row_read)):
                                itr_count += 1

                                if (col + 1) == int(data[metadata_index]['masking']['columns'][mask_col]['position']):

                                    # Track position of masked columns sequentially for optimization
                                    masked_col_position = col

                                    # Mask column values
                                    if data[metadata_index]['masking']['columns'][mask_col]['type'] == 'Shuffle':
                                        row_write[col] = Mask.shuffle(row_read[col])
                                    elif data[metadata_index]['masking']['columns'][mask_col]['type'] == 'ShuffleDet':
                                        row_write[col] = Mask.shuffle_det(row_read[col])
                                    elif data[metadata_index]['masking']['columns'][mask_col]['type'] == \
                                            'SubstitutionChar':
                                        row_write[col] = Mask.substitution_char(row_read[col])
                                    elif data[metadata_index]['masking']['columns'][mask_col]['type'] == \
                                            'SubstitutionCharDet':
                                        row_write[col] = Mask.substitution_char_det(row_read[col])
                                    break

                    # Skip masking for header record
                    '''elif data[metadata_index]['header_present'] == 'Yes' and rec_count == 0:
                        log.info("Processing HEADER Record...")
                        row_write = []

                        # Loop through trailer columns
                        for col in range(int(data[metadata_index]['header_column_count'])):
                            row_write.append(row_read[col])

                        # Reinitialize writer for header column names
                        writer = csv.writer(file_write, delimiter=data[metadata_index]['delimiter'],
                                            quoting=csv.QUOTE_NONE)

                    # Skip masking for trailer record
                    else:
                        log.info("Processing TRAILER Record...")
                        row_write = []

                        # Loop through trailer columns
                        for col in range(int(data[metadata_index]['trailer_column_count'])):
                            row_write.append(row_read[col])

                        # Reinitialize writer for trailer column names
                        writer = csv.writer(file_write, delimiter=data[metadata_index]['delimiter'],
                                            quoting=csv.QUOTE_NONE)'''

                    log.debug(row_write)
                    writer.writerow(row_write)
                    rec_count += 1
                    if (rec_count == file_rec_count - 1) or ((rec_count % 10000) == 0):
                        log.info("# of Records Processed: " + str(rec_count))
                        log.info("# of Iterations: " + str(itr_count))

        log.debug("mask_data_by_col_position() | <END>")


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
