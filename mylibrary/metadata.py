# 03 May 2018 | File Metadata Library

"""File Metadata Library
Library that:
1. Gets index # of object to be masked from metadata
2. Gets metadata and logs details
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
                if self.source_type == 'File_DL' or self.source_type == 'File_FW':
                    if data[record]['file_name'] == self.source_name:
                        log.debug("get_metadata_index() | <END>")
                        return record
                elif self.source_type == 'Table':
                    if data[record]['table_name'] == self.source_name:
                        log.debug("get_metadata_index() | <END>")
                        return record

            log.debug("get_metadata_index() | <END>")
            return -1

    def get_metadata(self, metadata_index):
        """Retrieves file metadata"""
        log.debug("get_metadata() | <START>")

        # Read File | Metadata
        with open(self.metadata_source) as meta_file:
            data = json.load(meta_file)

            for record in range(len(data)):

                if record == metadata_index:

                    if self.source_type == 'File_DL':
                        log.info('File Name: ' + data[record]['file_name'])
                        log.info('Delimiter: ' + data[record]['delimiter'])
                        log.info('Header Present: ' + data[record]['header_present'])
                        log.info('Header Column Count: ' + data[record]['header_column_count'])
                        log.info('Trailer Present: ' + data[record]['trailer_present'])
                        log.info('Trailer Column Count: ' + data[record]['trailer_column_count'])
                        log.info('Mask By Column Name: ' + data[record]['mask_by_column_name'])
                        log.info('Mask By Column Position: ' + data[record]['mask_by_column_position'])
                    elif self.source_type == 'File_FW':
                        log.info('File Name: ' + data[record]['file_name'])
                        log.info('Header Present: ' + data[record]['header_present'])
                        log.info('Header Column Count: ' + data[record]['header_column_count'])
                        log.info('Trailer Present: ' + data[record]['trailer_present'])
                        log.info('Trailer Column Count: ' + data[record]['trailer_column_count'])
                    elif self.source_type == 'Table':
                        log.info('Table Name: ' + data[record]['table_name'])
                        log.info('Schema: ' + data[record]['schema'])
                        log.info('Filter: ' + data[record]['filter'])

                    for column in range(len(data[record]['masking']['columns'])):
                        if self.source_type == 'File_FW':
                            log.info('\tColumn Position: ' +
                                     str(data[record]['masking']['columns'][column]['position_start']) + ' to ' +
                                     str(data[record]['masking']['columns'][column]['position_end']))
                        else:
                            log.info('\tColumn Name: ' + data[record]['masking']['columns'][column]['name'])
                            log.info('\tColumn Position: ' + str(data[record]['masking']['columns'][column]['position']))

                        log.info('\t\tMasking Type: ' + data[record]['masking']['columns'][column]['type'])
            log.debug("get_metadata() | <START>")
            return data
