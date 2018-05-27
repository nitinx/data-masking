# 01 May 2018 | Data Masker

"""Data Masker
Application that:
1. Retrieves file metadata
2. Reads data files and creates masked files based on metadata
"""

import logging
from mylibrary.metadata import Metadata
from mylibrary.traverse_file import FileDelimited
from mylibrary.traverse_table import Oracle
from time import gmtime, strftime

log = logging.getLogger(__name__)

#source_type = 'File'
#source_name = 'sampledata.csv'
source_type = 'Table'
source_name = 'zmt_collections'
schema = 'PY'

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

    # Determine Metadata Source
    metadata_source = 'metadata_' + str.lower(source_type) + '.json'

    # Retrieve File Metadata
    Metadata = Metadata(metadata_source, source_type, source_name)
    metadata_index = Metadata.get_metadata_index()
    data = Metadata.get_metadata()

    if source_type == 'File':
        # Read and Write Data File
        FileDelimited = FileDelimited(source_name)
        if data[metadata_index]['mask_by_column_name'] == 'Yes':
            FileDelimited.mask_data_by_col_name(data, metadata_index, FileDelimited.record_count())
        else:
            FileDelimited.mask_data_by_col_position(data, metadata_index, FileDelimited.record_count())
    else:
        # Read and Write Table Data
        Oracle = Oracle(source_name, schema)
        Oracle.mask_data(data, metadata_index, Oracle.get_record_count(data, metadata_index))

    print(strftime("%Y-%b-%d %H:%M:%S", gmtime()) + " | [main()] <END>")
