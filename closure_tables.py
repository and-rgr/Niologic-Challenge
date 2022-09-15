#!/usr/bin/env python
# coding: utf-8

# This script expects the following 3 command line arguments to run:
#     1 - file_name: the name of the Excel file to read 
#     2 - db_name: the name of the database that we will connect to
#     3 - table_name: the name of the table that we will create


## LIBRARIES AND FUNCTIONS ##

import sqlite3
import pandas as pd
import sys

def extract_paths(dataframe):
    paths = []
    rows = dataframe.shape[0]
    columns = dataframe.shape[1]
    
    for i in range(columns):
        for j in range(i,columns):
            for k in range(rows):
                paths.append(dataframe.iloc[k,[i,j]].tolist())
    
    # we convert the paths list to a dataframe, in order to remove duplicates
    paths_df = pd.DataFrame(paths)
    paths_df.drop_duplicates(inplace=True, keep='first')
    # we then convert it back to a list, because that is the type that the executemany method expects
    paths = paths_df.values.tolist()
    
    return paths


## VARIABLES ##

file_name = sys.argv[1]
db_name = sys.argv[2]
table_name = sys.argv[3]


## READ FILE ## 

data = pd.read_excel(file_name)


## EXTRACT PATHS ##

paths = extract_paths(data)


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
