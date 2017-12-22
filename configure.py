"""
title           : configure.py
description     : Configure the database. This is not a module, it can be run.
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
from shutil import copy2
import settings
import initialize
import db_module as dbm
import date_module


def backupDB():
    try:
        ext = ".backup_" + date_module.getDateTime()
        backup_name = settings.db_name + ext 
        copy2(settings.db_dir + settings.db_name, settings.db_dir + backup_name)
    except:
        print(">> Taking backup failed")
        print(">> I don't recommend altering database")


def mainScreen():
    print("\nCHOOSE WHAT YOU WANT TO DO:")
    print("--------------------------------")
    print("[1] - Configure table 'lecturers'")
    print("[2] - Configure table 'courses'")
    print("[3] - Configure table 'assignments'")
    print("Press any other key to quit\n")
    print("--------------------------------")
    resp = input()
    return resp
    

def lecturersScreen():
    print("\nCHOOSE WHAT YOU WANT TO DO:")
    print("--------------------------------")
    print("[1] - Add table 'lecturers' manually")
    print("[2] - Add table 'lecturers' from file")
    print("[3] - Write contents of table 'lecturers' to file")
    print("Press any other key to go back")
    print("--------------------------------")
    resp = input()
    if resp == '1':
        addManuallyLecturers()
    elif resp == '2':
        addFromFileLecturers()
    elif resp== '3':
        writeLecturers()


def coursesScreen():
    print("\nCHOOSE WHAT YOU WANT TO DO:")
    print("--------------------------------")
    print("[1] - Add table 'courses' manually")
    print("[2] - Add table 'courses' from file")
    print("[3] - Write contents of table 'courses' to file")
    print("Press any other key to go back")
    print("--------------------------------")
    resp = input()
    if resp == '1':
        addManuallyCourses()
    elif resp == '2':
        addFromFileCourses()
    elif resp == '3':
        writeCourses()


def assignsScreen():
    print("\nCHOOSE WHAT YOU WANT TO DO:")
    print("--------------------------------")
    print("[1] - Add table 'assignments' manually")
    print("[2] - Add table 'assignments' from file")
    print("[3] - Write contents of table 'assignments' to file")
    print("[4] - Delete all data inside the table 'assignments'")
    print("Press any other key to go back")
    print("--------------------------------")
    resp = input()
    if resp == '1':
        addManuallyAssigns()
    elif resp == '2':
        addFromFileAssigns()
    elif resp == '3':
        writeAssigns()
    elif resp == '4':
        deleteAssigns()
        

###############################################################################

def addManuallyLecturers():
    db, c = dbm.connectDB(settings.db_dir + settings.db_name)
    if db is None:
        settings.logger.critical("Database connection failed")
        sys.exit("Database connection failed, the program will be terminated")
    dbm.describeTable(c, "lecturers")
    print(">> Enter values:")
    print("*************")
    
    while True:
        entry = {"name":'', "middle":'', "surname":'', "email":''}
        entry["name"] = input("\nEnter name:\n")
        entry["middle"] = input("Enter middle:\n")
        entry["surname"] = input("Enter surname:\n")
        entry["email"] = input("Enter email:\n")
        
        print("\nYour choices are as follows:")
        print("--------------------------------")
        print("name : {}".format(entry["name"]))
        print("middle : {}".format(entry["middle"]))
        print("surname : {}".format(entry["surname"]))
        print("email : {}".format(entry["email"]))
        print("--------------------------------")
        print("")
        
        resp = input("Do you agree? [Y/N]\n")
        if resp.lower() == 'y':
            try:
                c.execute("""INSERT INTO lecturers(name, middle, surname, email)
                             VALUES(?,?,?,?)""",(entry["name"],entry["middle"],entry["surname"],entry["email"]))
                db.commit()
            except Exception as e:
                db.rollback()
                print(">> Entry cannot be added")
                print(e)
            else:
                print(">> Entry successfully added")
        else:
            print(">> Entry has been discarded\n")
        resp = input("Do you want to continue? [Y/N]\n")
        if resp.lower() != 'y':
            break
    
    db.close()
            

def addManuallyCourses():
    db, c = dbm.connectDB(settings.db_dir + settings.db_name)
    if db is None:
        settings.logger.critical("Database connection failed")
        sys.exit("Database connection failed, the program will be terminated")
    dbm.describeTable(c, "courses")
    print(">> Enter values:")
    print("*************")
    
    while True:
        entry = {"code":'', "name":'', "term":'', "grade":''}
        entry["code"] = input("\nEnter code:\n")
        entry["name"] = input("Enter course name:\n")
        ans = input("Enter term: [G]üz / [B]ahar\n")
        if ans.lower() == 'g' or ans.lower() == "güz":
            entry["term"] = "Güz"
        else:
            entry["term"] = "Bahar"
        while True:
            entry["grade"] = input("Enter grade: [1],[2],[3],[4]\n")
            if entry["grade"] in ['1','2','3','4']:
                break
            else:
                print(">> Incorrect value!")
        
        print("\nYour choices are as follows:")
        print("--------------------------------")
        print("code : {}".format(entry["code"]))
        print("course name : {}".format(entry["name"]))
        print("term : {}".format(entry["term"]))
        print("grade : {}".format(entry["grade"]))
        print("--------------------------------")
        print("")
        
        resp = input("Do you agree? [Y/N]\n")
        if resp.lower() == 'y':
            try:
                c.execute("""INSERT INTO courses(code, name, term, grade)
                             VALUES(?,?,?,?)""",(entry["code"],entry["name"],entry["term"],entry["grade"]))
                db.commit()
            except Exception as e:
                db.rollback()
                print(">> Entry cannot be added")
                print(e)
            else:
                print(">> Entry successfully added")
        else:
            print(">> Entry has been discarded\n")
        resp = input("Do you want to continue? [Y/N]\n")
        if resp.lower() != 'y':
            break
    
    db.close()


def addManuallyAssigns():
    db, c = dbm.connectDB(settings.db_dir + settings.db_name)
    if db is None:
        settings.logger.critical("Database connection failed")
        sys.exit("Database connection failed, the program will be terminated")
    dbm.describeTable(c, "assignments")
    print(">> Enter values:")
    print("*************")
    
    while True:
        entry = {"code":'', "lecturer name":'', "lecturer surname":'', "type":'', 
                 "grup":'', "course_id":'', "lecturer_id":'', "date":''}
        
        entry["code"] = input("\nEnter code:\n")
        c.execute("""SELECT course_id FROM courses WHERE code = ?""", (entry["code"],))
        res = c.fetchone()
        if res is None:
            print(">> This code is not in the database")
            resp = input("Do you want to continue? [Y/N]\n")
            if resp.lower() == 'y':
                continue
            else:
                break
        else:
            entry["course_id"] = res[0]
        
        
        entry["lecturer name"] = input("Enter lecturer name:\n")
        entry["lecturer surname"] = input("Enter lecturer surname:\n")
        c.execute("""SELECT lecturer_id FROM lecturers WHERE name = ?
                      AND surname = ?""", (entry["lecturer name"],entry["lecturer surname"]))
        res = c.fetchone()
        if res is None:
            print(">> This lecturer is not in the database")
            resp = input("Do you want to continue? [Y/N]\n")
            if resp.lower() == 'y':
                continue
            else:
                break
        else:
            entry["lecturer_id"] = res[0]
        
        ans = input("Enter type: [Ö]rgün / [İ]kinci\n")
        if ans.lower() == 'ö' or ans.lower() == "örgün" or ans.lower() == "örgün öğretim":
            entry["type"] = "Örgün Öğretim"
        else:
            entry["type"] = "İkinci Öğretim"
            
        while True:
            entry["grup"] = input("Enter group: [], [A],[B],[C],[D]\n").upper()
            if entry["grup"] in ['','A','B','C','D']:
                break
            else:
                print(">> Incorrect value!")
        
        entry["date"] = date_module.getDateTime()
        
        print("\nYour choices are as follows:")
        print("--------------------------------")
        print("code : {}".format(entry["code"]))
        print("course_id : {}".format(entry["course_id"]))
        print("lecturer name : {}".format(entry["lecturer name"]))
        print("lecturer surname : {}".format(entry["lecturer surname"]))
        print("lecturer_id : {}".format(entry["lecturer_id"]))
        print("type : {}".format(entry["type"]))
        print("group : {}".format(entry["grup"]))
        print("date : {}".format(entry["date"]))
        print("--------------------------------")
        print("")
        
        resp = input("Do you agree? [Y/N]\n")
        if resp.lower() == 'y':
            try:
                c.execute("""INSERT INTO assignments(course_id, lecturer_id, type, grup, date)
                             VALUES(?,?,?,?,?)""",(entry["course_id"],entry["lecturer_id"],entry["type"],entry["grup"],entry["date"]))
                db.commit()
            except Exception as e:
                db.rollback()
                print(">> Entry cannot be added")
                print(e)
            else:
                print(">> Entry successfully added")
        else:
            print(">> Entry has been discarded\n")
        resp = input("Do you want to continue? [Y/N]\n")
        if resp.lower() != 'y':
            break
    
    db.close()

###############################################################################

def addFromFileLecturers():
    print("\nINFO:")
    print("--------------------------------")
    print("Prepare a file named 'lecturers.txt' inside {} folder".format(settings.user_dir))
    print("Write data to each line of the file as follows:")
    print("")
    print("Name Middle Surname Email")
    print("'or'")
    print("Name Surname Email")
    print("")
    print("Example:")
    print("İhsan Oktay Anar anar@mail.com.tr")
    print("Hikmet Onat onat@mail.com.tr")
    print("--------------------------------")
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        fpath = settings.user_dir + "lecturers.txt"
        if os.path.isfile(fpath):
            db, c = dbm.connectDB(settings.db_dir + settings.db_name)
            if db is None:
                settings.logger.critical("Database connection failed")
                sys.exit("Database connection failed, the program will be terminated")
            num_row = 0
            num_added = 0
            with open(fpath, 'r') as f:
                for line in f:
                    # Ignore empty lines
                    if line.strip() == '':
                        continue
                    #
                    num_row +=1
                    data = line.split()
                    if len(data) == 4:
                        name = data[0]
                        middle = data[1]
                        surname = data[2]
                        email = data[3]
                        try:
                            c.execute("""INSERT INTO lecturers(name, middle, surname, email)
                                         VALUES(?,?,?,?)""",(name, middle, surname, email))
                            db.commit()
                        except Exception as e:
                            db.rollback()
                            print(">> Entry {} cannot be added".format(num_row))
                            settings.logger.debug("Entry {} {} cannot be added".format(name,surname))
                            settings.logger.error(str(e))
                        else:
                            num_added +=1
                            print(">> Entry {} successfully added".format(num_row))
                            settings.logger.debug("Entry {} {} successfully added".format(name,surname))
                    elif len(data) == 3:
                        name = data[0]
                        surname = data[1]
                        email = data[2]
                        try:
                            c.execute("""INSERT INTO lecturers(name, middle, surname, email)
                                         VALUES(?,?,?,?)""",(name, '', surname, email))
                            db.commit()
                        except Exception as e:
                            db.rollback()
                            print(">> Entry {} cannot be added".format(num_row))
                            settings.logger.debug("Entry {} {} cannot be added".format(name,surname))
                            settings.logger.error(str(e))
                        else:
                            num_added +=1
                            print(">> Entry {} successfully added".format(num_row))
                            settings.logger.debug("Entry {} {} successfully added".format(name,surname))
                    else:
                        print(">> Entry {} is not in the right format".format(num_row))
                        settings.logger.error("Entry number {} is not in the right format".format(num_row))
            db.close()
            print("\n>> Completed")
            print(">> {} out of {} rows have been added to the database".format(num_added, num_row))
            print(">> Check log file for errors\n")
            settings.logger.info("{} out of {} rows have been added to the database".format(num_added, num_row))                        
        else:
            print(">> The file does not exist ... Aborting")
    

def addFromFileCourses():
    print("\nINFO:")
    print("--------------------------------")
    print("Prepare a file named 'courses.txt' inside {} folder".format(settings.user_dir))
    print("Write data to each line of the file as follows:")
    print("")
    print("Code Name Term Grade")
    print("")
    print("Example:")
    print("EM101 Bilgisayar Programlama Güz 1")
    print("! Codes should not be seperated like 'EM 101'")
    print("! Term should be 'Güz' or 'Bahar'")
    print("! Grade should be between 1 and 4")
    print("--------------------------------")
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        fpath = settings.user_dir + "courses.txt"
        if os.path.isfile(fpath):
            db, c = dbm.connectDB(settings.db_dir + settings.db_name)
            if db is None:
                settings.logger.critical("Database connection failed")
                sys.exit("Database connection failed, the program will be terminated")
            num_row = 0
            num_added = 0
            with open(fpath, 'r') as f:
                for line in f:
                    # Ignore empty lines
                    if line.strip() == '':
                        continue
                    #
                    num_row +=1
                    data = line.split()
                    if "Güz" in data:
                        ind = data.index("Güz")
                        code = data[0]
                        course_name = ' '.join(data[1:ind])
                        term = data[ind]
                        try:
                            grade = data[ind+1]
                            if grade not in ['1', '2', '3', '4']:
                                raise Exception("Grade data is not between 1-4")
                        except Exception as e:
                            settings.logger.debug("Entry {} {} cannot be added".format(code,course_name))
                            settings.logger.error(str(e))
                            print(">> Entry {} cannot be added".format(num_row))
                            continue
                        try:
                            c.execute("""INSERT INTO courses(code, name, term, grade)
                                         VALUES(?,?,?,?)""",(code, course_name, term, grade))
                            db.commit()
                        except Exception as e:
                            db.rollback()
                            print(">> Entry {} cannot be added".format(num_row))
                            settings.logger.debug("Entry {} {} cannot be added".format(code, course_name))
                            settings.logger.error(str(e))
                        else:
                            num_added +=1
                            print(">> Entry {} successfully added".format(num_row))
                            settings.logger.debug("Entry {} {} successfully added".format(code, course_name))
                    elif "Bahar" in data:
                        ind = data.index("Bahar")
                        code = data[0]
                        course_name = ' '.join(data[1:ind])
                        term = data[ind]
                        try:
                            grade = data[ind+1]
                            if grade not in ['1', '2', '3', '4']:
                                raise Exception("Grade data is not between 1-4")
                        except Exception as e:
                            settings.logger.debug("Entry {} {} cannot be added".format(code,course_name))
                            settings.logger.error(str(e))
                            print(">> Entry {} cannot be added".format(num_row))
                            continue
                        try:
                            c.execute("""INSERT INTO courses(code, name, term, grade)
                                         VALUES(?,?,?,?)""",(code, course_name, term, grade))
                            db.commit()
                        except Exception as e:
                            db.rollback()
                            print(">> Entry {} cannot be added".format(num_row))
                            settings.logger.debug("Entry {} {} cannot be added".format(code, course_name))
                            settings.logger.error(str(e))
                        else:
                            num_added +=1
                            print(">> Entry {} successfully added".format(num_row))
                            settings.logger.debug("Entry {} {} successfully added".format(code, course_name))
                    else:
                        settings.logger.debug("Entry {} {} cannot be added".format(code,course_name))
                        settings.logger.error("Entry number {} is not in the right format".format(num_row))
                        print(">> Entry {} cannot be added".format(num_row))
        
            db.close()
            print("\n>> Completed")
            print(">> {} out of {} rows have been added to the database".format(num_added, num_row))
            print(">> Check log file for errors\n")  
            settings.logger.info("{} out of {} rows have been added to the database".format(num_added, num_row))                      
        else:
            print(">> The file does not exist ... Aborting")


def addFromFileAssigns():
    print("\nINFO:")
    print("--------------------------------")
    print("Prepare a file named 'assignments.txt' inside {} folder".format(settings.user_dir))
    print("Write data to each line of the file as follows:")
    print("")
    print("Course_code Lecturer_name Lecturer_surname Type Group")
    print("")
    print("Example:")
    print("EM101 Hüseyin Tevfik İkinci A")
    print("FİZ101 Metin Erksan Örgün")
    print("! Do not include middle names")
    print("! Group can be empty as in the above example")
    print("! İ and Ö can be used as acronyms for İkinci and Örgün")
    print("--------------------------------")
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        fpath = settings.user_dir + "assignments.txt"
        if os.path.isfile(fpath):
            db, c = dbm.connectDB(settings.db_dir + settings.db_name)
            if db is None:
                settings.logger.critical("Database connection failed")
                sys.exit("Database connection failed, the program will be terminated")
            num_row = 0
            num_added = 0
            with open(fpath, 'r') as f:
                for line in f:
                    # Ignore empty lines
                    if line.strip() == '':
                        continue
                    #
                    num_row +=1
                    data = line.split()
                    if len(data) == 5:
                        code = data[0]
                        lname = data[1]
                        lsurname = data[2]
                        ctype = data[3]
                        group = data[4].upper()
                        
                        if ctype == 'Ö' or ctype == "Örgün":
                            _type = "Örgün Öğretim"
                        elif ctype == 'İ' or ctype == "İkinci":
                            _type = "İkinci Öğretim"
                        else:
                            print(">> Entry {} cannot be added".format(num_row))
                            settings.logger.debug("Entry {} (group {}) cannot be added".format(code, group))
                            settings.logger.error("Entry type is not in the right format")
                            continue
                        
                        if group not in ['A','B','C','D']:
                            print(">> Entry {} cannot be added".format(num_row))
                            settings.logger.debug("Entry {} (group {}) cannot be added".format(code, group))
                            settings.logger.error("Entry group is not in the right format")
                            continue
                        
                        c.execute("""SELECT lecturer_id FROM lecturers WHERE name = ?
                                     AND surname = ?""",(lname, lsurname))
                        res = c.fetchone()
                        if res is None:
                            print(">> Entry {} cannot be added".format(num_row))
                            settings.logger.debug("Entry {} (group {}) cannot be added".format(code, group))
                            settings.logger.error("Lecturer name and surname cannot be found in the database")
                            continue
                        lecturer_id = res[0]
                        
                        c.execute("""SELECT course_id FROM courses WHERE code = ?""",(code,))
                        res = c.fetchone()
                        if res is None:
                            print(">> Entry {} cannot be added".format(num_row))
                            settings.logger.debug("Entry {} (group {}) cannot be added".format(code, group))
                            settings.logger.error("Course name cannot be found in the database")
                            continue
                        course_id = res[0]
                        
                        date = date_module.getDateTime()
                        
                        try:
                            c.execute("""INSERT INTO assignments(course_id, lecturer_id, type, grup, date)
                                         VALUES(?,?,?,?,?)""",(course_id, lecturer_id, _type, group, date))
                            db.commit()
                        except Exception as e:
                            db.rollback()
                            print(">> Entry {} cannot be added".format(num_row))
                            settings.logger.debug("Entry {} (group {}) cannot be added".format(code, group))
                            settings.logger.error(str(e))
                        else:
                            num_added +=1
                            print(">> Entry {} successfully added".format(num_row))
                            settings.logger.debug("Entry {} (group {}) successfully added".format(code, group))
                    
                    elif len(data) == 4:
                        code = data[0]
                        lname = data[1]
                        lsurname = data[2]
                        ctype = data[3]
                        group = ''
                        
                        if ctype == 'Ö' or ctype == "Örgün":
                            _type = "Örgün Öğretim"
                        elif ctype == 'İ' or ctype == "İkinci":
                            _type = "İkinci Öğretim"
                        else:
                            print(">> Entry {} cannot be added".format(num_row))
                            settings.logger.debug("Entry {} cannot be added".format(code))
                            settings.logger.error("Entry type is not in the right format")
                            continue
                        
                        c.execute("""SELECT lecturer_id FROM lecturers WHERE name = ?
                                     AND surname = ?""",(lname, lsurname))
                        res = c.fetchone()
                        if res is None:
                            print(">> Entry {} cannot be added".format(num_row))
                            settings.logger.debug("Entry {} cannot be added".format(code))
                            settings.logger.error("Lecturer name and surname cannot be found in the database")
                            continue
                        lecturer_id = res[0]
                        
                        c.execute("""SELECT course_id FROM courses WHERE code = ?""",(code,))
                        res = c.fetchone()
                        if res is None:
                            print(">> Entry {} cannot be added".format(num_row))
                            settings.logger.debug("Entry {} cannot be added".format(code))
                            settings.logger.error("Course name cannot be found in the database")
                            continue
                        course_id = res[0]
                        
                        date = date_module.getDateTime()
                        
                        try:
                            c.execute("""INSERT INTO assignments(course_id, lecturer_id, type, grup, date)
                                         VALUES(?,?,?,?,?)""",(course_id, lecturer_id, _type, group, date))
                            db.commit()
                        except Exception as e:
                            db.rollback()
                            print(">> Entry {} cannot be added".format(num_row))
                            settings.logger.debug("Entry {} cannot be added".format(code))
                            settings.logger.error(str(e))
                        else:
                            num_added +=1
                            print(">> Entry {} successfully added".format(num_row))
                            settings.logger.debug("Entry {} successfully added".format(code))
                    else:  
                        print(">> Entry {} cannot be added".format(num_row))
                        settings.logger.debug("Entry {} cannot be added".format(code))
                        settings.logger.error("Course name cannot be found in the database")
                        
            db.close()
            print("\n>> Completed")
            print(">> {} out of {} rows have been added to the database".format(num_added, num_row))
            print(">> Check log file for errors\n")                        
            settings.logger.info("{} out of {} rows have been added to the database".format(num_added, num_row))
        else:
            print(">> The file does not exist ... Aborting")
                        
                        
###############################################################################

def writeLecturers():
    print("\nINFO:")
    print("--------------------------------")
    print("""The contents of the 'lecturers' table will be written to a file named
          'lecturers_info.txt' under the folder '{}'""".format(settings.db_dir))
    print("--------------------------------")
    print("")
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        db, c = dbm.connectDB(settings.db_dir + settings.db_name)
        if db is None:
            settings.logger.critical("Database connection failed")
            sys.exit("Database connection failed, the program will be terminated")
        try:
            c.execute("""SELECT * FROM lecturers""")
            data = c.fetchall()
            if data == []:
                print("\n>> The table seems to be empty, nothing will be written\n")
                with open(settings.db_dir + "lecturers_info.txt",'w') as f:
                    f.write("The table is empty!")
            else:
                with open(settings.db_dir + "lecturers_info.txt",'w') as f:
                    for row in data:
                        for val in row:
                            f.write(str(val))
                            f.write(' ')
                        f.write("\n")
                print("\n>> Contents have been successfully written\n")
        except Exception as e:
            print("\n>> An error occured:")
            print(str(e)+"\n")
        finally:
            db.close()


def writeCourses():
    print("\nINFO:")
    print("--------------------------------")
    print("""The contents of the 'courses' table will be written to a file named""",
          """'courses_info.txt' under the folder '{}'""".format(settings.db_dir))
    print("--------------------------------")
    print("")
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        db, c = dbm.connectDB(settings.db_dir + settings.db_name)
        if db is None:
            settings.logger.critical("Database connection failed")
            sys.exit("Database connection failed, the program will be terminated")
        try:
            c.execute("""SELECT * FROM courses""")
            data = c.fetchall()
            if data == []:
                print("\n>> The table seems to be empty, nothing will be written\n")
                with open(settings.db_dir + "courses_info.txt",'w') as f:
                    f.write("The table is empty!")
            else:
                with open(settings.db_dir + "courses_info.txt",'w') as f:
                    for row in data:
                        for val in row:
                            f.write(str(val))
                            f.write(' ')
                        f.write("\n")
                print("\n>> Contents have been successfully written\n")
        except Exception as e:
            print("\n>> An error occured:")
            print(str(e)+"\n")
        finally:
            db.close()


def writeAssigns():
    print("\nINFO:")
    print("--------------------------------")
    print("""The contents of the 'assignments' table will be written to a file named""",
          """'assignments_info.txt' under the folder '{}'""".format(settings.db_dir))
    print("The output will be in readable format, i.e., course_id and lecturer_id", 
          "will be replaced by the corresponding values")
    print("--------------------------------")
    print("")
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        db, c = dbm.connectDB(settings.db_dir + settings.db_name)
        if db is None:
            settings.logger.critical("Database connection failed")
            sys.exit("Database connection failed, the program will be terminated")
        try:
            c.execute("""SELECT * FROM assignments""")
            data = c.fetchall()
            if data == []:
                print("\n>> The table seems to be empty, nothing will be written\n")
                with open(settings.db_dir + "assignments_info.txt",'w') as f:
                    f.write("The table is empty!")
            else:
                with open(settings.db_dir + "assignments_info.txt",'w') as f:
                    for row in data:
                        assign_id = str(row[0])
                        course_id = row[1]
                        lecturer_id = row[2]
                        _type = row[3]
                        grup = row[4]
                        date = row[5]
                        course = _returnCourse(c, course_id)
                        lecturer = _returnLecturer(c, lecturer_id)
                        f.write(' '.join([assign_id, course, lecturer, _type, grup, date]))
                        f.write("\n")
                        
                print("\n>> Contents have been successfully written\n")
        except Exception as e:
            print("\n>> An error occured:")
            print(str(e)+"\n")
        finally:
            db.close()
            

def _returnCourse(cursor, course_id):
    cursor.execute("""SELECT code, name FROM courses WHERE course_id = ?""",(course_id,))
    data = cursor.fetchone()
    return data[0] + ' '+  data[1]


def _returnLecturer(cursor, lecturer_id):
    cursor.execute("""SELECT name, middle, surname FROM lecturers WHERE lecturer_id = ?""",(lecturer_id,))
    data = cursor.fetchone()
    return data[0] + ' ' + data[1] + ' ' + data[2]

###############################################################################

def deleteAssigns():
    print("\nINFO:")
    print("--------------------------------")
    print("THIS WILL DELETE ALL ROWS OF TABLE 'assignments'")
    print("USE AUTOMATICALLY CREATED BACKUP INSIDE THE {} FOLDER IF YOU WANT TO UNDO".format(settings.db_dir))
    print("--------------------------------")
    print("")
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        db, c = dbm.connectDB(settings.db_dir + settings.db_name)
        if db is None:
            settings.logger.critical("Database connection failed")
            sys.exit("Database connection failed, the program will be terminated")
        try:    
            c.execute("""DELETE FROM assignments""")
            db.commit()
            print(">> All rows have been deleted!")
        except Exception as e:
            print(">> Rows cannot be deleted")
            print(">> An error occured:")
            print(str(e))
        finally:
            db.close()


###############################################################################

if __name__ == "__main__":
    initialize.init()
    print("\n")
    backupDB()
    settings.logger.debug("Running configuration program")
    while True:
        resp = mainScreen()
        if resp == '1':
            lecturersScreen()
        elif resp == '2':
            coursesScreen()
        elif resp == '3':
            assignsScreen()
        else:
            sys.exit()
            
