# 01 May 2018 | Data Masker

"""Data Masker
Application that:
1. Accepts SOURCE_TYPE and SOURCE_NAME as mandatory parameters. SCHEMA is an optional parameter. Where:
   - SOURCE_TYPE could be either 'File_DL' (delimited files) or 'File_FW' (fixed-width files) or 'Table' (Oracle Relational Table).
   - SOURCE_NAME is the name of the file/table
   - SCHEMA is the Oracle Schema of the table (applicable only for tables)
2. Retrieves metadata of the file/table to be masked from the .json metadata/configuration file
2. Based on SOURCE_TYPE and metadata, invokes the appropriate libraries to read, mask and generate masked files
"""

import logging
from mylibrary.metadata import Metadata
from mylibrary.traverse_file_dl import FileDelimited
from mylibrary.traverse_file_fw import FileFixedWidth
from mylibrary.traverse_table import Oracle
from time import gmtime, strftime

log = logging.getLogger(__name__)

#source_type = 'File_DL'
#source_name = 'sampledata_pos10000.csv'
source_type = 'File_FW'
source_name = 'sampledata_fw10000.dat'
#source_type = 'Table'
#source_name = 'zmt_collections'
#schema = 'PY'

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
    data = Metadata.get_metadata(metadata_index)

    if source_type == 'File_DL':
        # Read and Write File | Delimited
        FileDelimited = FileDelimited(source_name)
        if data[metadata_index]['mask_by_column_name'] == 'Yes':
            FileDelimited.mask_by_col_name(data, metadata_index, FileDelimited.record_count())
        else:
            FileDelimited.mask_by_col_position(data, metadata_index, FileDelimited.record_count())
    elif source_type == 'File_FW':
        # Read and Write File | Fixed Width
        FileFixedWidth = FileFixedWidth(source_name)
        FileFixedWidth.mask_by_col_position(data, metadata_index, FileFixedWidth.record_count())
    else:
        # Read and Write Table Data
        Oracle = Oracle(source_name, schema)
        Oracle.mask_data(data, metadata_index, Oracle.get_record_count(data, metadata_index))

    print(strftime("%Y-%b-%d %H:%M:%S", gmtime()) + " | [main()] <END>")
