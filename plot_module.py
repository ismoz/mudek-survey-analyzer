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

# This is required to prevent random crashes due to pylatex
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib
import uuid
import settings


# Pie chart auto percentage label controller
def my_autopct(pct):
    return ("%1.1f%%" % pct) if pct > settings.pie_pct_limit else ""


def preparePie(result):
    labels=settings.choices
    occurences = []
    for item in labels:
        occurences.append(result.count(item))
    
    matplotlib.rcParams.update({'font.size': settings.font_pie})
    colors = settings.colors
    
    #fig = plt.figure()
    plt.rcParams["figure.figsize"] = settings.figsize_pie
    ax = plt.subplot(111)
    
    pie = plt.pie(occurences, colors = colors, startangle=140, 
                  autopct=my_autopct, wedgeprops = {"linewidth": 1, "edgecolor" :"k" })
    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    
    plt.legend(pie[0], labels, loc="center left", bbox_to_anchor=(1, 0.5))
    
    figname = str(uuid.uuid4())+".pdf"
    plt.savefig(settings.temp_dir+figname, dpi=300, bbox_inches="tight")
    plt.close() # This is important! Otherwise you open many figures in the memory
    return figname


def prepareBar(result):
    labels=settings.choices
    occurences = []
    for item in labels:
        occurences.append(result.count(item))
    
    matplotlib.rcParams.update({'font.size': settings.font_bar})
    colors = settings.colors
    
    plt.rcParams["figure.figsize"] = settings.figsize_bar
    fig, ax = plt.subplots()
    x = [i for i in range(len(labels))]
    rects = ax.bar(x, occurences, color=colors, width = 0.6)
    # Add rect labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.02*height,
                "{}".format(int(height)), ha='center', va='bottom')
    #
    plt.ylim((0, max(occurences)+2))
    plt.xticks(x, labels, rotation=45)
    plt.yticks([])
    
    figname = str(uuid.uuid4())+".pdf"
    plt.savefig(settings.temp_dir+figname, dpi=300, bbox_inches="tight")
    plt.close() # This is important! Otherwise you open many figures in the memory
    return figname
        
        