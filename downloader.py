"""
title           : .py
description     : 
author          : Ismail Ozturk
email           : ismailozturk@erciyes.edu.tr
date created    : 21/11/2017
date modified   : 
version         : 1.0
python_version  : 3.4.4
notes           : 
change history  :
"""

import os
import urllib.request 
import urllib.parse
import shutil
import re
import settings


def downloadCSV():
    urls = _getURLs()
    if urls:
        num_url = 0
        num_success = 0
        print(">> Getting the URLs")
        for url in urls:
            num_url += 1
            settings.logger.debug("Downloading URL number {}".format(num_url))
            status = download(url)
            if status == 0:
                print(">> URL number {} has been successfully downloaded".format(num_url))
                num_success += 1
            else:
                print(">> URL number {} cannot be downloaded".format(num_url))
        
        settings.logger.debug("Finished downloading URLs")        
        print("\n>> {} out of {} URLs have been downloaded".format(num_success, num_url))
        print(">> Check log file for errors\n")
    

def _getURLs():
    urls = []
    if os.path.isfile(settings.user_dir + "urls.txt"):
        settings.logger.debug("Getting the URLs")
        with open(settings.user_dir + "urls.txt", 'r') as f:
            for line in f:
                # Ignore empty lines
                if line.strip() == '':
                    continue
                #
                urls.append(line)
    else:
        settings.logger.warning("The 'urls.txt' file does not exist under the '{}' folder".format(settings.user_dir))
        print(">> The 'urls.txt' file does not exist")   

    return urls         
    

def download(url):

    header={}
    header['User-Agent']='Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    req = urllib.request.Request(url,headers=header)
    
    try:
        resp = urllib.request.urlopen(req)
    except Exception as e: 
        settings.logger.error(str(e))
        return 1
        
    meta_data = resp.info()
    # If this stops working you have to recheck all meta data again
    #for key, item in meta_data.items():
    #    print("{} : {}".format(key, item))
    
    # The following meta data contains the UTF-8 file name
    contents_raw = meta_data["Content-Disposition"]
    
    # The meta data is url encoded so you should unquote it to
    # convert into meaningfull UTF-8 data
    contents = urllib.parse.unquote(contents_raw)
    
    # You find this pattern by investigating the contents data beforehand
    pattern = re.compile(r"UTF-8''(.*) \(Yanıtlar\)")
    value = pattern.search(contents)
    
    if value is None:
        settings.logger.error("File name cannot be resolved from meta data")
        return 1
    else:
        filename = value.group(1)
        filename = filename.strip()
        filename += ".csv"
        try:
            with urllib.request.urlopen(url) as response:
                with open(settings.csv_dir + filename,'wb') as fobj:
                    shutil.copyfileobj(response,fobj) # Default buffer size 16kB=16*1024 bytes
        except Exception as e:
            settings.logger.error(str(e))
            return 1
        
        settings.logger.debug("The URL has been successfully downloaded")
        return 0