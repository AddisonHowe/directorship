# Directorship Analysis
Construct a graph representation of firms and directors.

## Input Data

The input data to the program should be a .csv file with a header row and the following fields.

1. Firm ID
2. Firm name
3. Director Full Name
4. Director First Name
5. Director Middle Name
6. Director Last Name
7. Director Suffix
8. Director Address

The particular columns that these fields occupy is flexible. Adjustable variables are available in csv_reader.py which allow the user to specify which columns correspond to these fields.

Tables must use 0 for a null value.


## File Structure

The following file structure is assumed. The ```data/input``` directory will hold all .csv files containing tables to be read. Each time the program is run, there will be a folder name specified into which all output will be placed. Such folders will be found in ```data/output```, and will contain a logs folder, as well as two .csv files, the edge lists for the director and firm graphs. 

The ```data/input``` and ```data/output``` default directories can be changed, as demonstrated below.

    .
    ├── data
    │    ├── input
    │    │     ├── 1920_data.csv
    │    │     └── 1940_data.csv
    │    └── output
    │          ├── 1920
    │          │    ├── logs
    │          │    │     ├── all_directors.txt
    │          │    │     ├── merged_directors.txt
    │          │    │     └── ...
    │          │    ├── directors_edge_list.csv
    │          │    └── firms_edge_list.csv
    │          └── 1940
    │               ├── logs
    │               │     ├── all_directors.txt
    │               │     ├── merged_directors.txt
    │               │     └── ...
    │               ├── directors_edge_list.csv
    │               └── firms_edge_list.csv
    └── ...
    
    

## Installation and Requirements

This program requires python 3.8.

Clone the repo from https://github.com/AddisonHowe/directorship.

```bash
git clone https://github.com/AddisonHowe/directorship.git && cd directorship
```
If using conda, activate the desired environment and run
```bash
pip install .
```

## Usage

At the top of csv_reader.py, are the lines

    FIRM_ID_COL = 0
    FIRM_NAME_COL = 2
    FULL_NAME_COL = 1
    FIRST_COL = 10
    MIDDLE_COL = 11
    LAST_COL = 12
    SUFFIX_COL = 16
    ADDRESS_COL = 5
    
These values correspond to the columns of the input .csv value, and can be adjusted depending on the particular .csv being read. 

To run the program from the command line, use the command

    directorship <input_file.csv> <output_directory>

Include ```-d``` and/or ```-f``` to write the director edge list or firm edge list, respectively. Include ```-a ``` to write a list of aliases. For example, if reading the file 1940_data.csv located in the input directory and writing output to the folder 1940, including 
both edge lists, run

    directorship 1940_data.csv 1940 -f -d

You will be prompted to confirm that the output folder will be 
overwritten. Enter yes to continue, or no to abort.

This will use the default input/output directories. To instead use arbitrary locations for the input and output directories, include the optional arguments as follows

    directorship <input_file.csv> <output_directory> --indir <input-prefix> --outdir <output-prefix>

This will result in the folder ```output_directory``` being created within the directory specified by ```output-prefix```. The input file ```input_file.csv``` is assumed to exist within the directory specified by ```input-prefix```.

To get help, run

    directorship -h

## Misc.

Addison Howe 

Distributed under the MIT license. See ``LICENSE`` for more information.
