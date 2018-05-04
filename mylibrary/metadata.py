# 03 May 2018 | File Metadata Library

"""File Metadata Library
Library that:
"""

import json
import logging

log = logging.getLogger(__name__)


class Metadata:

    def get_fileindex(self):
        """Retrieves file index"""
        log.debug("get_fileindex() | <START>")
        with open('filemetadata.json') as meta_file:
            data = json.load(meta_file)

            log.debug("get_fileindex() | <END>")
            return 0

    def get_metadata(self):
        """Retrieves file metadata"""
        log.debug("get_metadata() | <START>")

        # Read File | Metadata
        with open('filemetadata.json') as meta_file:
            data = json.load(meta_file)

            for file in range(len(data)):
                log.info('Filename: ' + data[file]['filename'])
                log.info('Delimiter: ' + data[file]['delimiter'])
                log.info('Has Header: ' + data[file]['header'])
                log.info('Has Trailer: ' + data[file]['trailer'])
                log.info('Field Count: ' + str(data[file]['field_count']))

                for field in range(len(data[file]['masking']['fields'])):
                    log.info('\tFieldname: ' + data[file]['masking']['fields'][field]['name'])
                    log.info('\t\tMasking Type: ' + data[file]['masking']['fields'][field]['type'])
            log.debug("get_metadata() | <START>")
            return data
