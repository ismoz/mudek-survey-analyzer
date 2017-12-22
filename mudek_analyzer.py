"""
title           : mudek_analyzer.py
description     : Main program.
author          : Ismail Ozturk
email           : ismailozturk@erciyes.edu.tr
date created    : 12/11/2017
date modified   : 17/12/2017
version         : 1.1
python_version  : 3.4.4
notes           : 
change history  : --- v1.1 ---
                  - Added more options for sending email    
"""

import os, sys
import shutil
import initialize
import settings
import classes
import csv_reader
import pdf_module
import finalize
import downloader
import mailer
import archiever


def mainScreen():
    print("\nCHOOSE WHAT YOU WANT TO DO:")
    print("--------------------------------")
    print("[1] - Download URLs")
    print("[2] - Create PDF report for all CSV files")
    print("[3] - Create PDF report from single CSV file")
    print("[4] - Send PDF reports via email")
    print("[5] - Archieve PDF reports")
    print("Press any other key to quit\n")
    print("--------------------------------")
    resp = input()
    return resp


def singleCSVScreen():
    print("\nCHOOSE WHAT YOU WANT TO DO:")
    print("--------------------------------")
    print("[1] - Create PDF report using database")
    print("[2] - Create PDF report without using database")
    print("Press any other key to quit\n")
    print("--------------------------------")
    resp = input()
    if resp == '1':
        singleCSVwithDB()
    elif resp == '2':
        singleCSV()


# The actual function is located inside another module
def downloadScreen():
    print("\nINFO:")
    print("--------------------------------")
    print("This will download all the URLs inside the 'urls.txt' file", 
          "located under the '{}' folder".format(settings.user_dir)) 
    print("--------------------------------")
    print("")
    
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        downloader.downloadCSV()
        

def emailScreen():
    print("\nCHOOSE WHAT YOU WANT TO DO:")
    print("--------------------------------")
    print("[1] - Send a single PDF report via email")
    print("[2] - Send all PDF reports via email")
    print("[3] - Send PDF reports via email for grade 1")
    print("[4] - Send PDF reports via email for grade 2")
    print("[5] - Send PDF reports via email for grade 3")
    print("[6] - Send PDF reports via email for grade 4")
    print("[7] - Send PDF reports via email for grades 1-2")
    print("[8] - Send PDF reports via email for grades 1-2-3")
    print("--------------------------------")
    resp = input()
    if resp == '1':
        singleEmailSend()
    elif resp == '2':
        multiEmailSend()
    elif resp == '3':
        multiEmailSendChoice(1)
    elif resp == '4':
        multiEmailSendChoice(2)
    elif resp == '5':
        multiEmailSendChoice(3)
    elif resp == '6':
        multiEmailSendChoice(4)
    elif resp == '7':
        multiEmailSendChoice(12)
    elif resp == '8':
        multiEmailSendChoice(123)
        
        
###############################################################################

def singleCSV():
    print("\nINFO:")
    print("--------------------------------")
    print("This will create a PDF report from a single CSV file. The name of the", 
          "file does not matter. The final PDF does not contain any data about", 
          "the course.")
    print("--------------------------------")
    print("")
    
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        fname = input("Enter the file name:\n")
        print("")
        
        if os.path.isfile(settings.csv_dir + fname):
            questions, results = csv_reader.readCSV(fname)
            status = pdf_module.writeReportFree(fname.split('.')[0], questions, results)
            if status == 0:
                print(">> File has been written successfully")
                finalize.final()
            else:
                print(">> File cannot be written. See log for errors")
        else:
            print(">> The file does not exist in its path!")
    

def singleCSVwithDB():
    print("\nINFO:")
    print("--------------------------------")
    print("This will create a PDF report from a single CSV file. The name of the",
          "file should be in the appropriate format.")
    print("EX:")
    print("EM101_Bilg Prog_Ö.csv")
    print("EM102_Dev Analizi_Ö_A.csv")
    print("--------------------------------")
    print("")
    
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        fname = input("Enter the file name:\n")
        print("")
        
        if os.path.isfile(settings.csv_dir + fname):
            course = classes.Course(fname)
            if course.valid:
                questions, results = csv_reader.readCSV(fname)
                status = pdf_module.writeReport(course, questions, results)
                if status == 0:
                    print(">> File has been written successfully\n")
                    print("Course information:")
                    print("Course Code      : {}".format(course.course_code))
                    print("Course Name      : {}".format(course.course_name))
                    print("Course Type      : {}".format(course.course_type))
                    print("Course Group     : {}".format(course.course_group))
                    print("Course Term      : {}".format(course.course_term))
                    print("Course Grade     : {}".format(course.course_grade))
                    print("Lecturer Name    : {}".format(course.lecturer_name + ' ' + course.lecturer_middle))
                    print("Lecturer Surname : {}".format(course.lecturer_surname))
                    print("Lecturer Email   : {}".format(course.lecturer_email))
                    print("")
                    finalize.final()
                else:
                    print(">> File cannot be written. See log for errors")
            else:
                print(">> The CSV file cannot be recognized. Check file name or database")
        else:
            print(">> The file does not exist in its path!")


def multiCSVwithDB():
    print("\nINFO:")
    print("--------------------------------")
    print("This will create PDF reports for all CSV files inside the",
          "'{}' folder.".format(settings.csv_dir))
    print("CSV file names should be in appropriate formats as in the following examples.")
    print("EX:")
    print("EM101_Bilg Prog_Ö.csv")
    print("EM102_Dev Analizi_Ö_A.csv")
    print("--------------------------------")
    print("")
    
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        settings.logger.debug("Starting PDF report creation for all CSV files")
        files = csv_reader.getCSVNames()
        if files:
            num_success = 0
            num_file = 0
            for file in files:
                num_file += 1
                settings.logger.debug("Creating class for file {}".format(file))
                course = classes.Course(file)
                
                if course.valid:
                    settings.logger.debug("Class created successfully")
                else:
                    settings.logger.warning("Class cannot be created for file {}".format(file))
                    settings.logger.error("Check file name '{}' or database!".format(file))
                    print(">> PDF report creation is not possible for file {}".format(file))
                    continue
                
                settings.logger.debug("Reading file {}".format(file))
                questions, results = csv_reader.readCSV(file)
                settings.logger.debug("Attempting to create PDF report for {}".format(file))
                status = pdf_module.writeReport(course, questions, results)
                
                if status == 0:
                    num_success += 1
                    settings.logger.debug("PDF report successfully created")
                    print(">> PDF report successfully created for file {}".format(file))
                else:
                    settings.logger.warning("PDF report creation FAILED!")
                    print(">> PDF report creation FAILED for file {}".format(file))
            
            print("\n>> PDF reports have been created for {} out of {} CSV files".format(num_success, num_file))
            print(">> Check log file for errors")
            settings.logger.info("PDF reports have been created for {} out of {} CSV files".format(num_success, num_file))
            settings.logger.debug("Ending PDF report generation")
            finalize.final()
            
        else:
            settings.logger.debug("The folder does not contain any CSV files")
            print(">> The folder does not contain any CSV files")
        

###############################################################################

def singleEmailSend():
    print("\nINFO:")
    print("--------------------------------")
    print("This will send a PDF report via email. The PDF file name ",
          "should be in the usual format as in the examples. ",
          "The receiver address will be taken from the database.")
    print("EX:")
    print("EM101_Bilg Prog_Ö.pdf")
    print("EM102_Dev Analizi_Ö_A.pdf")
    print("--------------------------------")
    print("")
    
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        while True:
            sender_addr, passwd = mailer.getLoginInfo()
            if sender_addr is None:
                print(">> Login failed!")
                resp = input("\nDo you want to continue? [Y/N]\n")
                if resp.lower() != 'y':
                    break
            else:
                break
    
        if sender_addr is not None:
            fname = input("Enter the file name:\n")
            print("")
            
            if os.path.isfile(settings.pdf_dir + fname):
                course = classes.Course(fname)
                if course.valid:
                    print(">> The PDF report will be send to the following lecturer:")
                    print("Lecturer Name    : {}".format(course.lecturer_name + ' ' + course.lecturer_middle))
                    print("Lecturer Surname : {}".format(course.lecturer_surname))
                    print("Lecturer Email   : {}".format(course.lecturer_email))
                    print("")
                    resp = input("\nDo you agree? [Y/N]\n")
                    if resp.lower() == 'y':
                        status = mailer.sendAttachMail(course, sender_addr, passwd)
                        if status == 0:
                            print(">> PDF report has been sent successfully!")
                        else:
                            print(">> PDF report could not be sent! Check log for errors")
                else:
                    print(">> Necessary data cannot be retrieved from the database. Check file name or database!")        
            else:
                print(">> The file does not exist in its path!")


def multiEmailSend():
    print("\nINFO:")
    print("--------------------------------")
    print("This will send all PDF reports inside the {} folder via email. ".format(settings.pdf_dir), 
          "The PDF file names should be in the usual format as in the examples. ",
          "The receiver addresses will be taken from the database. ",
          "So do not forget to check the assignments table!")
    print("EX:")
    print("EM101_Bilg Prog_Ö.pdf")
    print("EM102_Dev Analizi_Ö_A.pdf")
    print("--------------------------------")
    print("")
    
    print("WARNING: FREE EMAIL SERVERS ONLY ALLOWS SENDING A LIMITED NUMBER OF ", 
          "REMOTE MAILS (100 EMAILS PER DAY FOR GMAIL). SO BE CAREFUL ABOUT THE TOTAL ", 
          "NUMBER OF PDF REPORTS!")
    print("")
    
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        settings.logger.debug("USER ATTEMPTED TO SEND ALL PDF REPORTS VIA EMAIL!")
        settings.logger.debug("Retrieving SMTP server login credentials")
        while True:
            print("")
            sender_addr, passwd = mailer.getLoginInfo()
            if sender_addr is None:
                print(">> Login failed!")
                resp = input("\nDo you want to continue? [Y/N]\n")
                if resp.lower() != 'y':
                    break
            else:
                break
    
        if sender_addr is not None:  
            settings.logger.debug("Login is successfull; attempting to send PDF reports via email")
            pdf_files = []
            for file in os.listdir(settings.pdf_dir):
                if file.endswith(".pdf"):
                    pdf_files.append(file)
            
            num_files = 0
            num_success = 0
            for file in pdf_files:
                num_files += 1
                course = classes.Course(file)
                if course.valid:
                    settings.logger.debug("Sending {} to {}".format(file, course.lecturer_email))
                    print("Sending {} to {} ... ".format(file, course.lecturer_email), end='')
                    status = mailer.sendAttachMail(course, sender_addr, passwd)
                    if status == 0:
                        num_success += 1
                        print("[Ok]")
                    else:
                        print("[Failed]")
                else:
                    settings.logger.warning("{} cannot be retrieved. Check file name or database!".format(file))
                    print("{} cannot be retrieved. Check file name or database!".format(file)) 
        
            print("\n>> {} out of {} PDF reports have been sent successfully".format(num_success, num_files))
            print(">> Check log file for errors")
            settings.logger.info("{} out of {} PDF reports have been sent successfully".format(num_success, num_files))
            settings.logger.debug("Ending sending emails")
        else:
            settings.logger.debug("Failed retrieving login credentials")


def multiEmailSendChoice(choice):
    print("\nINFO:")
    print("--------------------------------")
    print("This will send specific PDF reports inside the {} folder via email. ".format(settings.pdf_dir), 
          "The PDF file names should be in the usual format as in the examples. ",
          "The receiver addresses will be taken from the database. ",
          "So do not forget to check the assignments table!")
    print("EX:")
    print("EM101_Bilg Prog_Ö.pdf")
    print("EM102_Dev Analizi_Ö_A.pdf")
    print("--------------------------------")
    print("")
    
    print("NOTE: THIS WILL SEND PDF REPORTS ONLY FOR GRADES {}\n".format('-'.join(str(choice))))
    
    resp = input("\nDo you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        settings.logger.debug("USER ATTEMPTED TO SEND PDF REPORTS VIA EMAIL FOR GRADES {}".format('-'.join(str(choice))))
        settings.logger.debug("Retrieving SMTP server login credentials")
        while True:
            print("")
            sender_addr, passwd = mailer.getLoginInfo()
            if sender_addr is None:
                print(">> Login failed!")
                resp = input("\nDo you want to continue? [Y/N]\n")
                if resp.lower() != 'y':
                    break
            else:
                break
    
        if sender_addr is not None:  
            settings.logger.debug("Login is successfull; attempting to send PDF reports via email")
            pdf_files = []
            for file in os.listdir(settings.pdf_dir):
                if file.endswith(".pdf"):
                    pdf_files.append(file)
            
            num_files = 0
            num_success = 0
            for file in pdf_files:
                course = classes.Course(file)
                if course.valid:
                    if str(course.course_grade) in str(choice):
                        num_files += 1
                        settings.logger.debug("Sending {} to {}".format(file, course.lecturer_email))
                        print("Sending {} to {} ... ".format(file, course.lecturer_email), end='')
                        status = mailer.sendAttachMail(course, sender_addr, passwd)
                        if status == 0:
                            num_success += 1
                            print("[Ok]")
                        else:
                            print("[Failed]")
                else:
                    settings.logger.warning("{} cannot be retrieved. Check file name or database!".format(file))
                    print("{} cannot be retrieved. Check file name or database!".format(file)) 
        
            print("\n>> {} out of {} PDF reports have been sent successfully".format(num_success, num_files))
            print(">> Check log file for errors")
            settings.logger.info("{} out of {} PDF reports have been sent successfully".format(num_success, num_files))
            settings.logger.debug("Ending sending emails")
        else:
            settings.logger.debug("Failed retrieving login credentials")
        

###############################################################################

def archieve():
    print("\nINFO:")
    print("--------------------------------")
    print("This will archieve PDF reports inside the {} folder. ".format(settings.archieve_dir),
          "This operation also sorts reports according to their grade and type.")
    print("--------------------------------")
    print("")

    resp = input("Do you want to continue? [Y/N]\n")
    if resp.lower() == 'y':
        
        print("\n>> All files should be deleted inside the {} folder ".format(settings.archieve_dir),
              "before this operation!")
        
        resp = input("Do you agree? [Y/N]\n")
        if resp.lower() == 'y':
            _emptyArchieveFolder()
            archiever.archievePDFReports()
            
            resp = input("Do you also want to create a zip file? [Y/N]\n")
            if resp.lower() == 'y':
                bname = input("Enter the base name for the zip file:\n")
                if bname == '':
                    bname = "default_name"
                try:
                    shutil.make_archive(bname, "zip", settings.archieve_dir)
                    print("\n>> Zip file created successfully")
                except Exception as e:
                    print("Zip file cannot be created:")
                    print(str(e))
                else:
                    fullname = bname+".zip"
                    shutil.copy2(fullname, settings.archieve_dir)
                    os.remove(fullname)


def _emptyArchieveFolder():
    for obj in os.listdir(settings.archieve_dir):
        obj_path = os.path.join(settings.archieve_dir, obj)
        try:
            if os.path.isfile(obj_path):
                if obj.endswith(".zip"):
                    continue
                os.remove(obj_path)
            elif os.path.isdir(obj_path):
                shutil.rmtree(obj_path)
        except Exception as e:
            print("The path {} cannot be deleted:".format(obj_path))
            print(str(e))

###############################################################################

if __name__ == "__main__":
    
    initialize.init()
    settings.logger.debug("Running main program")
    
    print("")
    print("#############################################################")
    print("#            __   ___          __        __        ___      #")
    print("# |\/| |  | |  \ |__  |__/    /__` |  | |__) \  / |__  \ /  #")
    print("# |  | \__/ |__/ |___ |  \    .__/ \__/ |  \  \/  |___  |   #")
    print("#                                __  ___  __                #")
    print("#         /\  |\ |  /\  |    \ /  / |__  |__)               #")
    print("#        /~~\ | \| /~~\ |___  |  /_ |___ |  \               #")
    print("#                                                           #")
    print("#############################################################")
    print("# Version: {}                                              #".format(settings.version))
    print("# Author : Ismail OZTURK    <i.ozturk@yandex.com>           #")
    print("#############################################################")
    print("")
    
    while True:
        resp = mainScreen()
        if resp == '1':
            downloadScreen()
        elif resp == '2':
            multiCSVwithDB()
        elif resp == '3':
            singleCSVScreen()
        elif resp == '4':
            emailScreen()
        elif resp == '5':
            archieve()
        else:
            sys.exit()