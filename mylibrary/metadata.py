# 03 May 2018 | File Metadata Library

"""File Metadata Library
Library that:
"""

import json
import logging

log = logging.getLogger(__name__)


class Metadata:

    def __init__(self, metadata_source, source_type, source_name):
        self.metadata_source = metadata_source
        self.source_type = source_type
        self.source_name = source_name

    def get_metadata_index(self):
        """Retrieves file index"""
        log.debug("get_metadata_index() | <START>")
        with open(self.metadata_source) as meta_file:
            data = json.load(meta_file)

            for record in range(len(data)):
                if self.source_type == 'File':
                    if data[record]['filename'] == self.source_name:
                        log.debug("get_metadata_index() | <END>")
                        return record
                    else:
                        if data[record]['tablename'] == self.source_name:
                            log.debug("get_metadata_index() | <END>")
                            return record

            log.debug("get_metadata_index() | <END>")
            return -1

    def get_metadata(self):
        """Retrieves file metadata"""
        log.debug("get_metadata() | <START>")

        # Read File | Metadata
        with open(self.metadata_source) as meta_file:
            data = json.load(meta_file)

            for record in range(len(data)):

                if self.source_type == 'File':
                    log.info('File Name: ' + data[record]['filename'])
                    log.info('Delimiter: ' + data[record]['delimiter'])
                    log.info('Has Header: ' + data[record]['header'])
                    log.info('Has Trailer: ' + data[record]['trailer'])
                    log.info('Column Count: ' + str(data[record]['column_count']))
                else:
                    log.info('Table Name: ' + data[record]['tablename'])
                    log.info('Schema: ' + data[record]['schema'])
                    log.info('Column Count: ' + str(data[record]['column_count']))


                for column in range(len(data[record]['masking']['columns'])):
                    log.info('\tColumn Name: ' + data[record]['masking']['columns'][column]['name'])
                    log.info('\t\tMasking Type: ' + data[record]['masking']['columns'][column]['type'])
            log.debug("get_metadata() | <START>")
            return data
