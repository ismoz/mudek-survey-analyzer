"""
title           : archiever.py
description     : Main program.
author          : Ismail Ozturk
email           : ismailozturk@erciyes.edu.tr
date created    : 12/11/2017
date modified   :
version         : 1.0
python_version  : 3.4.4
notes           : 
change history  :
"""

import os
import shutil
import settings
import classes


# Archieve Directory Tree:
first_layer = ["1._Sınıf", "2._Sınıf", "3._Sınıf", "4._Sınıf"]
second_layer = ["Örgün_Öğretim", "İkinci_Öğretim"]


def archievePDFReports():
    
    print("\n>> Archieving PDF reports")
    settings.logger.debug("Archieving operations started")
    
    pdf_files = []
    for file in os.listdir(settings.pdf_dir):
        if file.endswith(".pdf"):
            pdf_files.append(file)
    
    num_file = 0
    num_archieved = 0
    for file in pdf_files:
        num_file += 1
        course = classes.Course(file)
        if course.valid:
            src = settings.pdf_dir + file
            if course.course_grade == 1:
                dst = settings.archieve_dir + first_layer[0]
                if course.course_type == "Örgün Öğretim":
                    dst = os.path.join(dst, second_layer[0])
                elif course.course_type == "İkinci Öğretim":
                    dst = os.path.join(dst, second_layer[1])
                else:
                    settings.logger.error("Unexpected Course Instance")
                    continue
            elif course.course_grade == 2:
                dst = settings.archieve_dir + first_layer[1]
                if course.course_type == "Örgün Öğretim":
                    dst = os.path.join(dst, second_layer[0])
                elif course.course_type == "İkinci Öğretim":
                    dst = os.path.join(dst, second_layer[1])
                else:
                    settings.logger.error("Unexpected Course Instance")
                    continue
            elif course.course_grade == 3:
                dst = settings.archieve_dir + first_layer[2]
                if course.course_type == "Örgün Öğretim":
                    dst = os.path.join(dst, second_layer[0])
                elif course.course_type == "İkinci Öğretim":
                    dst = os.path.join(dst, second_layer[1])
                else:
                    settings.logger.error("Unexpected Course Instance")
                    continue
            elif course.course_grade == 4:
                dst = settings.archieve_dir + first_layer[3]
                if course.course_type == "Örgün Öğretim":
                    dst = os.path.join(dst, second_layer[0])
                elif course.course_type == "İkinci Öğretim":
                    dst = os.path.join(dst, second_layer[1])
                else:
                    settings.logger.error("Unexpected Course Instance")
                    continue
            else:
                continue
            
            settings.logger.debug("Copying PDF report {} to archieve folder".format(file))
            try:
                settings.logger.debug("Copied successfully")
                os.makedirs(dst, exist_ok = True)
                shutil.copy2(src, dst)
            except Exception as e:
                settings.logger.debug("Copy operation failed")
                settings.logger.error(str(e))
                print(">> PDF report {} cannot be archieved".format(file))
            else:
                num_archieved += 1
                print(">> PDF report {} has been archieved successfully".format(file))
                os.remove(src)
        else:
            print("Cannot retrieve data from {}".format(file))
            settings.logger.warning("Cannot retrieve data from {}. Check its name or database".format(file))
            
    print("\n>> {} out of {} PDF reports have been archieved inside the {} folder".format(num_archieved, num_file, settings.archieve_dir))
    print(">> Check log for errors\n")
    settings.logger.debug("{} out of {} PDF reports have been archieved".format(num_archieved, num_file))