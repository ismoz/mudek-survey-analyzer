"""
title           : db_module.py
description     : Generic SQLite Operations Module
author          : Ismail Ozturk
email           : ismailozturk@erciyes.edu.tr
date created    : 17/1/2017
date modified   :
version         : 1.0
python_version  : 3.4.4
notes           : createDB() has been altered for mudek analyser and Foreign keys are enabled
change history  :
"""
import os
import sqlite3 as sql


def createDB(db_name):
    try:
        db = sql.connect(db_name)
        db.close()
        print("Database created successfully")
        return 0
    except Exception as e:
        print(e)
        return 1


def connectDB(db_name):
    if os.path.isfile(db_name):
        try:
            db = sql.connect(db_name)
            cursor = db.cursor()
            db.execute("PRAGMA foreign_keys=ON") # Foreign keys enable
            return db, cursor
        except Exception as e:
            print(e)
            return None, None
    else:
        print("Database cannot be found. Check path")
        return None, None
            

def getTables(cursor):
    try:
        cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
        tables = cursor.fetchall()
        return [table[0] for table in tables]
    except Exception as e:
        print(e)
        return None
    

def showTables(cursor):
    print("Available tables :")
    tables = getTables(cursor)
    for table in tables:
        print("==> {}".format(table))


def _printColInfo(info):
    _id = info[0]
    name = info[1]
    _type = info[2]
    if (info[3]):
        notnull = "NOT NULL"
    else:
        notnull = ""
    default = info[4]
    if (info[5]):
        primary = "PRIMARY"
    else:
        primary = ""
    print("| ID = {_id} | NAME = {name} | TYPE = {_type} | DEFAULT = {default} | {notnull} | {primary} |".format(
            _id=_id, name=name, _type=_type, default=default, notnull=notnull, primary = primary))


def describeTable(cursor, table):
    try:
        cursor.execute("""PRAGMA table_info([{}])""".format(table))
        infos = cursor.fetchall()
            
    except Exception as e:
        print(e)
        return None
    
    else:
        print("Column Information For Table {} :".format(table))
        for info in infos:
            _printColInfo(info)


def getColumns(cursor, table):
    try:
        cursor.execute("""PRAGMA table_info([{}])""".format(table))
        infos = cursor.fetchall()
        return [info[1] for info in infos]
    except Exception as e:
        print(e)
        return None


def _genericInsertCommand(db, cursor, table, entries):
    cols = getColumns(cursor, table)
    cols.pop(0) # Remove primary key id
    if len(cols) != len(entries):
        print("Entries doesn't fit; nothing will be written")
    else:
        table_params = ','.join(list(cols))
        table_params = '(' + table_params
        table_params = table_params + ')'
        queries = ['?']*len(cols)
        queries = ','.join(queries)
        queries = '(' + queries
        queries = queries + ')'
        command = """INSERT INTO {table_name}{table_params} VALUES {queries}""".format(
                table_name = table, table_params = table_params, queries = queries)
        try:
            cursor.execute(command,tuple(entries))
            db.commit()
            print("Entries successfully added")
        except Exception as e:
            print(e)
            print("Nothing has been written")
            db.rollback()


def addManually(db, cursor, table):
    describeTable(cursor, table)
    while True:
        print("Add item for TABLE {} :".format(table))
        cols = getColumns(cursor, table)
        cols.pop(0)
        entries = []
        for col in cols:
            print("Enter {}".format(col))
            entry = input()
            entries.append(entry)
        print("\nYour choices are as follows:")
        print(entries)
        ans = input("Do you agree? [Y/N]\n")
        if ans.lower() == 'y':
            _genericInsertCommand(db, cursor, table, entries)
        ans = input("Do you want to continue? [Y/N]\n")
        if ans.lower() == 'n':
            break


def getNumOfRows(cursor, table):
    command = "SELECT COUNT(*) FROM {}".format(table)
    cursor.execute(command)
    val = cursor.fetchone()
    return val[0] # returns integer


def writeRows(cursor, table):
    try:
        command = "SELECT * FROM {}".format(table)
        cursor.execute(command)
        results = cursor.fetchall()
        cols = getColumns(cursor, table)
    except Exception as e:
        print(e)
    else:
        with open(table+".txt",'w') as f:
            f.write("Contents of table {}:\n".format(table))
            f.write(' '.join(str(val) for val in cols) + "\n\n")
            for result in results:
                f.write(' '.join(str(val) for val in result) + "\n")
        

            