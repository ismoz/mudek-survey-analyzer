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

import csv, os
import settings


def readCSV(fname):
    with open(settings.csv_dir+fname, encoding="utf-8") as f:
        reader = csv.reader(f)
        header_row = next(reader)
        questions = header_row[1:]
        
        num_questions = len(questions)
        results=[[] for i in range(num_questions+1)]
                           
        for row in reader:
            # Results should be lowercase
            for i, item in enumerate(row):
                row[i] = item.lower()
            #
            # settings.eliminate tumu ayni olan cevaplari iptal eder
            if (settings.eliminate) and (row[1:]==[settings.eliminate_choice]*num_questions):
                pass
            else:
                for i in range(num_questions+1):
                    results[i].append(row[i])
        
    # Get rid of the time stamps
    results.pop(0) 
            
    return questions, results


def getCSVNames():
    csv_files = []
    for file in os.listdir(settings.csv_dir):
        if file.endswith(".csv"):
            csv_files.append(file)
    
    return csv_files


    
    