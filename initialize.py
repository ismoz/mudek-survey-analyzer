"""
title           : .py
description     : 
author          : Ismail Ozturk
email           : ismailozturk@erciyes.edu.tr
date created    : 12/11/2017
date modified   :
version         : 1.0
python_version  : 3.4.4
notes           : 
change history  :
"""

import os, sys
import logging
import settings
import db_module as dbm


def init():
    _initDirectories()
    settings.logger = _getLogger()
    settings.logger.debug("Logging is available")
    settings.logger.debug("Checking database")
    _checkDatabase()
    settings.logger.debug("Connecting to database")
    db, c = dbm.connectDB(settings.db_dir + settings.db_name)
    if db is None:
        settings.logger.critical("Database connection failed")
        sys.exit("Database connection failed, the program will be terminated")
    settings.logger.debug("Checking tables")
    _checkTables(db, c)
    db.close()
    
    
def _initDirectories():
    sep = os.path.sep
    settings.csv_dir += sep
    settings.pdf_dir += sep
    settings.temp_dir += sep
    settings.zip_dir += sep
    settings.db_dir += sep
    settings.log_dir += sep
    settings.user_dir += sep
    settings.archieve_dir += sep
    
    settings.fig_path = ".." + sep + settings.temp_dir
    
    
def _checkDatabase():
    print("Checking database ... ",end='')
    if os.path.isfile(settings.db_dir + settings.db_name):
        print("[Ok]")
        settings.logger.debug("Database exists in its path")
    else:
        print("[Failed]")
        print("Creating database ... ", end='')
        settings.logger.debug("Database does not exist. Creating.")
        res = dbm.createDB(settings.db_dir + settings.db_name)
        if res !=  0:
            settings.logger.critical("Database creation failed")
            raise Exception("FATAL ERROR: Database could not be created")
        settings.logger.debug("Database has been created successfully")


def _getLogger():
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    file_h = logging.FileHandler(settings.log_dir + settings.log_file, mode = 'w')
    fmt = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt, '%d-%m-%Y %H:%M:%S')
    file_h.setFormatter(formatter)
    
    logger.addHandler(file_h)
    return logger


def _createTableLecturers(db, cursor):
    try:
        cursor.execute("""
                  CREATE TABLE lecturers(lecturer_id INTEGER PRIMARY KEY,
                                         name TEXT NOT NULL,
                                         middle TEXT DEFAULT '',
                                         surname TEXT NOT NULL,
                                         email TEXT NOT NULL,
                                         UNIQUE (name, surname))
        """)
        db.commit()
        # Note: I assume there are no lecturers with the same name and surname!
        # If there is you should handle one of them manually or modify the whole program
        settings.logger.debug("Table lecturers has been created")
    except Exception as e:
        db.rollback()
        db.close()
        settings.logger.critical("An error occured while creating table lecturers")
        raise e


def _createTableCourses(db, cursor):
    try:
        cursor.execute("""
                  CREATE TABLE courses(course_id INTEGER PRIMARY KEY,
                                       code TEXT NOT NULL,
                                       name TEXT NOT NULL,
                                       term TEXT NOT NULL,
                                       grade INTEGER NOT NULL,
                                       UNIQUE (code))
        """)
        db.commit()
        settings.logger.debug("Table courses has been created")
    except Exception as e:
        db.rollback()
        db.close()
        settings.logger.critical("An error occured while creating table courses")
        raise e


def _createTableAssignments(db, cursor):
    try:
        # group is reserved so I use grup in Turkish
        cursor.execute("""
                  CREATE TABLE assignments(assign_id INTEGER PRIMARY KEY,
                                       course_id INTEGER NOT NULL,
                                       lecturer_id INTEGER NOT NULL,
                                       type TEXT NOT NULL,
                                       grup TEXT DEFAULT '',
                                       date TEXT NOT NULL,
                                       FOREIGN KEY(course_id) REFERENCES courses(course_id),
                                       FOREIGN KEY(lecturer_id) REFERENCES lecturers(lecturer_id),
                                       UNIQUE (course_id, type, grup))
        """)
        db.commit()
        settings.logger.debug("Table assignments has been created")
    except Exception as e:
        db.rollback()
        db.close()
        settings.logger.critical("An error occured while creating table assignments")
        raise e
        

def _checkTables(db, cursor):
    print("Checking tables ... ", end='')
    tables = dbm.getTables(cursor)
    check_lecturers = "lecturers" in tables
    check_courses = "courses" in tables
    check_assignments = "assignments" in tables
    table_created_flag = False
    
    if check_lecturers:
        settings.logger.debug("Table lecturers is available in database")
    else:
        settings.logger.debug("Table lecturers is NOT available in database")
        settings.logger.debug("Creating table lecturers")
        _createTableLecturers(db, cursor)
        table_created_flag = True
    
    if check_courses:
        settings.logger.debug("Table courses is available in database")
    else:
        settings.logger.debug("Table courses is NOT available in database")
        settings.logger.debug("Creating table courses")
        _createTableCourses(db, cursor)
        table_created_flag = True
    
    if check_assignments:
        settings.logger.debug("Table assignments is available in database")
    else:
        settings.logger.debug("Table assignments is NOT available in database")
        settings.logger.debug("Creating table assignments")
        _createTableAssignments(db, cursor)
        table_created_flag = True
    
    if table_created_flag:
        settings.logger.debug("At least one table has just been created. Database should be configured.")
        print("[Failed]")
        if os.path.basename(os.path.basename(sys.argv[0])) == "configure.py":
            print("Tables are now available")
        else:
            sys.exit("You should configure database. Run configure.py")
    else:
        settings.logger.debug("All tables are available in database")
        print("[Ok]")


