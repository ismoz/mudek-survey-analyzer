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

import sys
import db_module as dbm
import settings


class Course():
    
    def __init__(self, file_name):
        
        settings.logger.debug("Creating a Course class")
        self.filename = file_name # Full file name: google form name + extension
        self.data = self._ignoreExt() # Google form name without extension
        settings.logger.debug("Course data is : {}".format(self.data))
        self._getDataAttributes()
        
        status = self._checkData()
        if status:
            db, c = dbm.connectDB(settings.db_dir + settings.db_name)
            if db is None:
                settings.logger.critical("Database connection failed")
                sys.exit("Database connection failed, the program will be terminated")
            
            self._getCourseAttributes(c)
            self._getLecturerAttributes(c)
            
            if self.course_id == "N/A" or self.lecturer_id == "N/A":
                self.valid = False
                settings.logger.debug("Course class is NOT valid!")
            else:
                self.valid = True
                settings.logger.debug("Course class is valid")
            
        else:
            self._setCourseAttributes(["N/A"]*4)
            self._setLecturerAttributes("N/A", ["N/A"]*4)
            self.valid = False
            settings.logger.debug("Course class is NOT valid because of the file name!")   
                
        
    def _ignoreExt(self):
        ls = self.filename.split('.')
        return ls[0]
    
    
    def _getDataAttributes(self):
        ls = self.data.split('_')
        if len(ls)==3:
            self.course_code = ls[0] # Dersin kodu
            self.course_alias = ls[1] # Dersin google form kisa adi
            self.course_type = ls[2] # Orgun / Ikinci ogretim 
            self.course_group = '' # A veya B
        elif len(ls)==4:
            self.course_code = ls[0]
            self.course_alias = ls[1]
            self.course_type = ls[2]
            self.course_group = ls[3]
        else:
            self.course_code = "N/A"
            self.course_alias = "N/A"
            self.course_type = "N/A"
            self.course_group = "N/A"
    
    
    def _checkData(self):
        if self.course_type in ['Ö', 'İ']:
            valid1 = True
            if self.course_type == 'Ö':
                self.course_type = "Örgün Öğretim"
            else:
                self.course_type = "İkinci Öğretim"
        else:
            valid1 = False
        
        if self.course_group in ['','A','B','C','D']:
            valid2 = True
        else:
            valid2 = False
            
        if self.course_code == "N/A" or self.course_alias == "N/A":
            valid3 = False
        else:
            valid3 = True
        
        return valid1 and valid2 and valid3
    
    
    def _getCourseAttributes(self, cursor):
        settings.logger.debug("Getting course attributes")
        try:
            cursor.execute("""SELECT course_id, name, term, grade FROM 
                              courses WHERE code = ?""", (self.course_code,))
            res = cursor.fetchone()
        except Exception as e:
            settings.logger.debug("An error occured while reading database")
            settings.logger.error(str(e))
            res = None
        
        if res is None:
            self._setCourseAttributes(["N/A"]*4)
            settings.logger.debug("Cannot retrieve course attributes")
        else:
            self._setCourseAttributes(res)
            settings.logger.debug("Course attributes have been read successfully")
    

    def _setCourseAttributes(self, attr_list):
        self.course_id = attr_list[0]
        self.course_name = attr_list[1]
        self.course_term = attr_list[2]
        self.course_grade = attr_list[3]
        
    
    def _getLecturerAttributes(self, cursor):
        if self.course_id == "N/A":
            self._setLecturerAttributes("N/A", ["N/A"]*4)
        else:
            settings.logger.debug("Getting lecturer attributes")
            try:
                cursor.execute("""SELECT lecturer_id FROM assignments WHERE course_id = ?
                               AND type = ? AND grup = ?""", (self.course_id, self.course_type, self.course_group))
                res1 = cursor.fetchone()
            except Exception as e:
                settings.logger.debug("An error occured while reading database")
                settings.logger.error(str(e))
                res1 = None
                
            if res1 is not None:
                try:
                    cursor.execute("""SELECT name, middle, surname, email FROM lecturers WHERE lecturer_id = ?""", res1)
                    res2 = cursor.fetchone()
                except Exception as e:
                    settings.logger.debug("An error occured while reading database")
                    settings.logger.error(str(e))
                    res2 = None
            else:
                res2 = None
            
            if res1 is None or res2 is None:
                self._setLecturerAttributes("N/A", ["N/A"]*4)
                settings.logger.debug("Cannot retrieve lecturer attributes")
            else:
                self._setLecturerAttributes(res1, res2)
                settings.logger.debug("Lecturer attributes have been read successfully")
                
    
    def _setLecturerAttributes(self, lecturer_id, attr_list):
        self.lecturer_id = lecturer_id
        self.lecturer_name = attr_list[0]
        self.lecturer_middle = attr_list[1]
        self.lecturer_surname = attr_list[2]
        self.lecturer_email = attr_list[3]
        
        
    
            
        