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

import datetime


# A standard for text type date and time data
def getDateTime():
    date = datetime.datetime.now()
    year = date.year
    day = date.day
    month = date.month
    hour = date.hour
    minute = date.minute
    
    data = "{:02d}_{:02d}_{}_{:02d}_{:02d}".format(day,month,year,hour,minute)
    return data