# 01 May 2018 | Data Masker

"""Data Masker
Application that:
1. Retrieves file metadata
2. Reads data files and creates masked files based on metadata
"""

import logging
from mylibrary.metadata import Metadata
from mylibrary.traverse import Delimited
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

    # Retrieve File Metadata
    Metadata = Metadata()
    file_index = Metadata.get_fileindex()
    data = Metadata.get_metadata()

    # Read and Write Data File
    Delimited = Delimited()
    Delimited.read_write_file(data, file_index)


    print(strftime("%Y-%b-%d %H:%M:%S", gmtime()) + " | [main()] <END>")
