# Data Masker


An application to mask sensitive data in flat files/Oracle Tables. Current features:

Masking Options:
1. Mask delimited files
   - by column names
   - by column positions
2. Mask fixed-width files by column positions
3. Mask Oracle Relational Tables and generate masked delimited file

Masking Routines:
1. Character Substitution - Random
2. Character Substitution - Deterministic
3. Character Shuffling - Random
4. Character Shuffling - Deterministic

Pre-Requisites
------------
1. Installation of Oracle DB - if Oracle table masking is to be used.

Installation
------------
This process is currently manual and involves the following steps:

    1. Copy over the .py files to the appropriate folders
    2. Place the delimited/fixed-width files in the folder containing application.py
	3. If Oracle masking functionality is to be leveraged, path to key file (Line #9) in db_oracle.py should be edited as appropriate. 
	
	Format of oracle.key file:
       [
	     {
		   "USER": "<PLACEHOLDER>",
		   "PASSWORD": "<PLACEHOLDER>",
		   "CONNECT_STRING": "<PLACEHOLDER>"
	     }
       ]

Usage Instructions
------------
Update the .json files and furnish the details of the files/tables to be masked. Samples provided below:
```
Delimited Files: metadata_file_dl.json

  - By Column Names
  
  [
    {
      "file_name": "sampledata.csv",
      "delimiter": ",",
      "header_present": "Yes",
      "header_column_count": "2",
      "trailer_present": "Yes",
      "trailer_column_count": "2",
      "date_format": "MM/DD/YYYY",
      "mask_by_column_name": "Yes",
      "mask_by_column_position": "No",
      "masking":
      {
        "columns":
        [
          { "name": "street", "position":0, "type": "Shuffle" },
          { "name": "city", "position":0, "type": "SubstitutionChar" },
          { "name": "zip", "position":0, "type": "ShuffleDet" },
          { "name": "email", "position":0, "type": "SubstitutionChar" },
          { "name": "telno", "position":0, "type": "SubstitutionChar" }
        ]
      }
    }
  ]
  
  - By Column Positions
  
  [
    {
      "file_name": "sampledata_pos.csv",
      "delimiter": ",",
      "header_present": "Yes",
      "header_column_count": "2",
      "trailer_present": "Yes",
      "trailer_column_count": "2",
      "date_format": "MM/DD/YYYY",
      "mask_by_column_name": "No",
      "mask_by_column_position": "Yes",
      "masking":
      {
        "columns":
        [
          { "name": "", "position": "2", "type": "Shuffle" },
          { "name": "", "position": "3", "type": "SubstitutionChar" },
          { "name": "", "position": "6", "type": "Shuffle" }
        ]
      }
    }
  ]

Fixed-width Files: metadata_file_fw.json

  [
    {
      "file_name": "sampledata_fw.dat",
      "header_present": "Yes",
      "header_column_count": "2",
      "trailer_present": "Yes",
      "trailer_column_count": "2",
      "date_format": "MM/DD/YYYY",
      "record_length": 47,
      "masking":
      {
        "columns":
        [
          { "position_start": 2, "position_end": 10, "type": "Shuffle" },
          { "position_start": 26, "position_end": 33, "type": "SubstitutionChar" }
        ]
      }
    }
  ] 
  
Oracle Tables: metadata_table.json

  [
    {
      "table_name": "zmt_collections",
      "schema": "PY",
      "filter": "WHERE PERIOD = '201805'",
      "masking":
      {
        "columns":
        [
          { "name": "COLLECTION_ID", "position":0, "type": "Shuffle" },
          { "name": "TITLE", "position":0, "type": "SubstitutionChar" }
        ]
      }
    }
  ]
```
  

In the Backlog
------------
1. Additional masking routines
2. Detailed Statistics
3. Visualization & Notifications
