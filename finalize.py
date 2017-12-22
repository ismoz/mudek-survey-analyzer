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
import settings


def tidyTemp():
    for file in os.listdir(settings.temp_dir):
        file_path = settings.temp_dir + file
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(e)


def final():
    if not settings.debug:
        tidyTemp()