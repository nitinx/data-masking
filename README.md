# Data Masker

### Overview
To enable quality test data in lower environments, there is a need bring down datasets from production. However, the datasets contain Personally identifiable information (PII) and would need to be masked before copying them over. A cofigurable app was required for this purpose.

#### Masking Options:
1. Delimited files
   - by column names
   - by column positions
2. Fixed-width files by column positions
3. Oracle Relational Tables (generates masked delimited file)

#### Masking Routines:
1. Character Substitution - Random
2. Character Substitution - Deterministic
3. Character Shuffling - Random
4. Character Shuffling - Deterministic

### Pre-Requisites

1. Configure Oracle keys (if Oracle masking is required).
2. Setup metadata for masking.

### Code

Seven Python files:

- `application.py`: Main application script.
- `db_oracle.py`: Module | Oracle connectivity.
- `mask.py`: Module | Retrieves metadata for masking.
- `metadata.py`: Module | Retrieves metadata for masking.
- `traverse_file_dl.py`: Module | Traverses delimited files. 
- `traverse_file_fw.py`: Module | Traverses fixed-width files.
- `traverse_table.py`: Module | Traverses Oracle relational tables.

### Configuration Files

If Oracle masking functionality is to be leveraged, create an Oracle key file in the format specified below:  

```	
Format of oracle.key file:
       [
	     {
		   "USER": "<PLACEHOLDER>",
		   "PASSWORD": "<PLACEHOLDER>",
		   "CONNECT_STRING": "<PLACEHOLDER>"
	     }
       ]
```

### Metadata Files [JSON format]

Three JSONs:

- `metadata_file_dl.json`: Metadata for delimited files.
- `metadata_file_fw.json`: Metadata for fixed-width files.
- `metadata_table.json`: Metadata for relational tables.

### Usage Instructions

Update JSONs and furnish the details of objects to be masked. Samples provided below:

Delimited Files [mask by column names]: metadata_file_dl.json
```
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
```  

Delimited Files [mask by column positions]: metadata_file_dl.json
```  
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
```

Fixed-width Files: metadata_file_fw.json
```
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
```
  
Oracle Tables: metadata_table.json
```
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
  

### Backlog
1. Additional masking routines
2. Detailed Statistics
3. Visualization & Notifications

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)
