"""
title           : .py
description     : 
author          : Ismail Ozturk
email           : ismailozturk@erciyes.edu.tr
date created    : 12/11/2017
date modified   : 21/11/2017
version         : 1.1
python_version  : 3.4.4
notes           : 
change history  :
"""

from pylatex import Document, Command, NoEscape, Figure, \
                    NewLine, SubFigure, HFill, TextColor
from pylatex.utils import bold, italic

import settings
import plot_module
    

def prepareDoc(course):
    geometry = settings.geometry
    title = "{} DERSİ DERS DEĞERLENDİRME ANKETİ SONUÇLARI".format(course.course_name)
    
    doc = Document(indent=False, geometry_options=geometry)
    doc.preamble.append(Command("usepackage","babel","turkish"))
    doc.preamble.append(Command("usepackage","float"))
    doc.preamble.append(Command("usepackage","framed"))
    doc.preamble.append(Command("title", title))
    doc.preamble.append(NoEscape(r"\date{\vspace{-1.5cm}\today}"))
    
    doc.append(NoEscape(r"\maketitle"))
    doc.append(Command("shorthandoff","="))
    
    doc.append(Command("begin", "framed"))
    doc.append(bold("Dersin Kodu : "))
    doc.append("{}".format(course.course_code))
    doc.append(NoEscape(r"\quad"))
    doc.append("({}. sınıf)".format(course.course_grade))
    doc.append(NewLine())
    doc.append(bold("Dersin Türü : "))
    doc.append("{}".format(course.course_type))
    doc.append(NewLine())
    doc.append(bold("Dersin Grubu : "))
    doc.append("{}".format(course.course_group))
    doc.append(NewLine())
    doc.append(bold("Dersin Dönemi : "))
    doc.append("{}".format(course.course_term))
    doc.append(NewLine())
    doc.append(bold("Öğretim Üyesi : "))
    lname = course.lecturer_name + ' ' + course.lecturer_middle + ' ' + course.lecturer_surname
    doc.append(lname)
    doc.append(Command("end", "framed"))
    
    return doc


# This doesn't depend on database or classes / used with writeReportFree
def prepareDocFree():
    geometry = settings.geometry
    
    doc = Document(indent=False, geometry_options=geometry)
    doc.preamble.append(Command("usepackage","babel","turkish"))
    doc.preamble.append(Command("usepackage","float"))
    doc.preamble.append(Command("title", "ANKET SONUÇLARI"))
    doc.preamble.append(NoEscape(r"\date{\vspace{-1.5cm}\today}"))
    
    doc.append(NoEscape(r"\maketitle"))
    doc.append(Command("shorthandoff","="))
    return doc


# obsolete
def writeFigure(doc, figname, soru_sayisi, scale):
    with doc.create(Figure(position="h!")) as fig:
        width = NoEscape(r"{}\textwidth".format(scale))
        fig.add_image(settings.fig_path + figname, width=width)
        fig.add_caption("Soru "+ str(soru_sayisi))


def createPdf(doc, filename, debug):
    try:
        doc.generate_pdf(settings.pdf_dir+filename, clean_tex=not(debug), compiler="pdflatex")
    except Exception as e:
        settings.logger.debug("PDF generation failed. Here is the error report:")
        settings.logger.error(str(e))
        return 1
    else:
        return 0
    

def writeQuestion(doc, question, result, figpie, figbar):
    doc.append(TextColor("blue",question))
    width_pie = NoEscape(r"{}\textwidth".format(settings.scale_pie))
    width_bar = NoEscape(r"{}\textwidth".format(settings.scale_bar))
    
    with doc.create(Figure(position="H")) as main_fig:    
        with doc.create(SubFigure(position='b')) as left_fig:
            left_fig.add_image(settings.fig_path + figbar, width = width_bar, placement=NoEscape("\centering"))
            left_fig.add_caption("")        
        #doc.append(HFill())    
        with doc.create(SubFigure(position='b')) as right_fig:
            right_fig.add_image(settings.fig_path + figpie, width = width_pie, placement=NoEscape("\centering"))
            right_fig.add_caption("")        
        main_fig.add_caption("")


# This will be used! course is an instance of Course() class
def writeReport(course, questions, results):
    filename = course.data
    doc = prepareDoc(course)
    for i in range(len(questions)):
        figpie = plot_module.preparePie(results[i])
        figbar = plot_module.prepareBar(results[i])
        writeQuestion(doc, questions[i], results[i], figpie, figbar)
    
    if settings.eliminate:
        doc.append(italic(bold("Not: ")))
        doc.append(italic("Değerlendirmeye hepsi '{}' olarak işaretlenmiş cevaplar katılmamıştır.".format(settings.eliminate_choice)))
        
    status = createPdf(doc, filename, settings.debug)
    return status


# This doesn't depend on classes or database
# filename is the name of the resulting pdf file (without .pdf)
def writeReportFree(filename, questions, results):
    doc = prepareDocFree()
    for i in range(len(questions)):
        figpie = plot_module.preparePie(results[i])
        figbar = plot_module.prepareBar(results[i])
        writeQuestion(doc, questions[i], results[i], figpie, figbar)
    
    if settings.eliminate:
        doc.append(italic(bold("Not: ")))
        doc.append(italic("Değerlendirmeye hepsi '{}' olarak işaretlenmiş cevaplar katılmamıştır.".format(settings.eliminate_choice)))
        
    status = createPdf(doc, filename, settings.debug)
    return status

###############################################################################
