# Niologic Challenge

Repository for the coding challenge at Niologic.

## Overview

We create a Closure Table in order to store the hierarchies described in the given file. Every row in the Closure Table corresponds to a path in the hierarchy tree, including paths of zero length.

EXCEL FILE &#8594; PYTHON SCRIPT &#8594; SQLITE DB

We are given the hierarchy structure as an Excel file. We process the file in the Python script, and extract all possible paths in the hierarchy graph. We then connect to the SQLite database, and add all paths, determined by their start point and end point, in the Closure Table.


## Prerequisites

We make use of the following Python libraries

  - sqlite3
  - pandas
  - sys
  
  
## Included Files  

  - **InputClosureTable.xlsx**: the Excel file containing the desired product hierarchy
  - **closure_tables.py**: the python script we use to create the closure table
  - **niologic.db**: the database created by the python script
  - **sql_statements.txt**: the edges and nodes of the hierarchy graph, represented as SQL statements


## Script Overview

Most of the work is done in the **extract_paths** function:
We loop over all column pairs, and over all rows, of the given table. The pairs we extract correspond to all the possible paths within the hierarchy graph, including those of length zero. We then remove any duplicate lines from the list. The output of the function is a list of lists.

From there, we connect to the SQLite database, create a new Closure Table, and add a new row, for every element in the output of the **extract_paths** function.

Finally, we use the output of **extract_paths** again, in order to store the edges and nodes of the hierarchy graph in a file, represented as SQL statements.

## Script Execution

The script can be run from the command line, using the following 3 command line arguments:
  - **1 - file_name**: the name of the Excel file to read 
  - **2 - db_name**: the name of the database that we will connect to
  - **3 - table_name**: the name of the table that we will create

We assume that the Excel file will be in the same path as the script. Both the database file and the text file that the script creates, will also be created in the same path as the script.

  
## Performance  

  The script runs in O(3) time. As an estimate, using 2 cores of a Ryzen 5 1600, we get the following values:
  
| rows  | seconds |
|-------|---------|
| 1536  | 11.71   |
| 12288 | 100.62  |
| 196608 | 1441.6 |
