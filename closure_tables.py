#!/usr/bin/env python
# coding: utf-8


## SCRIPT EXECUTION ##

"""
The script can be run from the command line, using the following 3 command line arguments, in order:

    file_name:  the name of the Excel file to read
    db_name:    the name of the database that we will connect to
    table_name: the name of the table that we will create

for example, to read the file InputClosureTable.xlsx, connect to the niologic database, and create a table called CLOSURE_TABLE, we will use the following command

    python closure_tables.py InputClosureTable.xlsx niologic CLOSURE_TABLE

We assume that the Excel file will be in the same path as the script. 
Both the database file and the text file that the script creates, will also be created in the same path as the script.
"""

## LIBRARIES AND FUNCTIONS ##

import sqlite3
import pandas as pd
import sys


def append_endpoints(row):
    # used to append the start points and end points to the "paths" variable
    paths.append(row.tolist())


def extract_paths(dataframe):
    # loops over the hierarchy table, and picks out the start points and end points of paths in the hierarchy graph
    rows = dataframe.shape[0]
    columns = dataframe.shape[1]
    
    for i in range(columns):
        for j in range(i,columns):
            x = dataframe.iloc[:,[i,j]]
            x.apply(append_endpoints, axis=1)
            
    return paths


def remove_duplicates(paths):
    # we convert the "paths" list to a dataframe, in order to remove duplicates
    paths_df = pd.DataFrame(paths)
    paths_df.drop_duplicates(inplace=True, keep='first')

    # we then convert it back to a list, because that is the type that the executemany method expects
    paths = paths_df.values.tolist()

    return paths


## VARIABLES ##

file_name = sys.argv[1]
db_name = sys.argv[2]
table_name = sys.argv[3]

# the paths that we extract from the hierarchy graph will be stored here, as lists of length 2
paths = []


## READ FILE ## 

data = pd.read_excel(file_name)


## EXTRACT PATHS ##

paths = extract_paths(data)
paths = remove_duplicates(paths)


## CONNECT TO DB ## 

connection = sqlite3.connect(db_name + ".db")
cursor = connection.cursor()


## CREATE & POPULATE TABLE ##

cursor.execute("CREATE TABLE IF NOT EXISTS " + table_name + " (ancestor TEXT, descendant TEXT)")
cursor.executemany("insert into " + table_name + " values (?,?)", paths)
connection.commit()


## SQL INSERT STATEMENTS ##

f = open("sql_statements.txt", "a")
f.write("INSERT INTO " + table_name + "\n")
f.write("VALUES" + "\n")
for i, row in enumerate(paths):
    if i < len(paths)-1:
        f.write("    (" + str(row[0]) + ", " + str(row[1]) + ")," + "\n")
    else:
        f.write("    (" + str(row[0]) + ", " + str(row[1]) + ");" + "\n")
f.close()
