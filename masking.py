# 01 May 2018 | Mask Delimited Files

import json
import csv
import logging
from time import gmtime, strftime

log = logging.getLogger(__name__)

if __name__ == '__main__':

    print(strftime("%Y-%b-%d %H:%M:%S", gmtime()) + " | [main()] <START>")

    # Logger | Initialize
    fmt_string = "%(asctime)s | %(levelname)s | %(module)s | %(message)s"
    fmtr = logging.Formatter(fmt=fmt_string)
    sh = logging.StreamHandler()
    sh.setFormatter(fmtr)
    my_lib_logger = logging.getLogger("mylibrary")
    my_lib_logger.addHandler(sh)

    # Logger | Set Level
    my_lib_logger.setLevel("INFO")

    with open('filemetadata.json') as meta_file:
        data = json.load(meta_file)

    # Read File | Metadata
    for file in range(len(data)):
        file_index = file
        print('Filename: ' + data[file]['filename'] + '\n'
              'Delimiter: ' + data[file]['delimiter'] + '\n'
              'Has Header: ' + data[file]['header'] + '\n'
              'Has Trailer: ' + data[file]['trailer'] + '\n'
              'Field Count: ' + str(data[file]['field_count']))

        for field in range(len(data[file]['masking']['fields'])):
            print('\t'
                  + 'Fieldname: ' + data[file]['masking']['fields'][field]['name'] + ' | '
                  + 'Mask Type: ' + data[file]['masking']['fields'][field]['type'])

    # Read File | Data
    with open('sampledata.csv', 'r', newline='') as file_read:

        # Check if file has header record
        snf = csv.Sniffer().has_header(file_read.read(100))
        print('Has Header?', snf)
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
                            row_write[fieldnames[field]] = 'MASKED'
                writer.writerow(row_write)

    print(strftime("%Y-%b-%d %H:%M:%S", gmtime()) + " | [main()] <END>")
