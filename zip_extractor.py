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

import os
import zipfile
import settings


def extractAll():
    zip_files = []
    for file in os.listdir(settings.zip_dir):
        if file.endswith(".zip"):
            zip_files.append(file)
    
    for file in zip_files:
        with zipfile.ZipFile(settings.zip_dir+file, 'r') as z:
            z.extractall(settings.csv_dir)