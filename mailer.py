import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

from email.header import Header
from email.encoders import encode_base64

from email.utils import formataddr
from email.utils import formatdate

import getpass
import settings


def getLoginInfo():
    settings.logger.debug("Taking login credentials fot the smtp server")
    print("Enter sender email & password for the smtp server!")
    sender_addr = input("Sender email : ")
    passwd = getpass.getpass()
    
    settings.logger.debug("Attempting to login into the smtp server")
    if _try_login(sender_addr, passwd) == 0:
        settings.logger.debug("Login is successful!")
        return sender_addr, passwd
    else:
        settings.logger.debug("Login failed!")
        return None, None
    
    
def _try_login(sender_addr, passwd):
    try:
        server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
        if settings.smtp_TLS:
            server.starttls()
        server.login(sender_addr, passwd)
        server.quit()
        return 0
    except:
        return 1


def sendAttachMail(course, sender_addr, passwd):
    fname = course.data + ".pdf"
    fname_enc = Header(fname, "utf-8").encode()
    
    if course.lecturer_middle == '':
        lec_name = " ".join([course.lecturer_name, course.lecturer_surname])
    else:
        lec_name = " ".join([course.lecturer_name, course.lecturer_middle, course.lecturer_surname])
    
    sender_name = Header(settings.smtp_sender_name, "utf-8").encode()
    recipient_name = Header(lec_name, "utf-8").encode()
    
    recipient_addr = course.lecturer_email
    
    subject = Header("Anket Sonuçları ({})".format(course.course_code), "utf-8").encode()
    
    msg = MIMEMultipart()
    msg["Date"] = formatdate(localtime=1)
    msg["From"] = formataddr((sender_name, sender_addr)) 
    msg["To"] = formataddr((recipient_name, recipient_addr)) 
    msg["Subject"] = subject
    
    
    
    body = settings.mail_body.format(name=course.course_name, _type=course.course_type, 
                                      group=course.course_group, contact=settings.mail_contact,
                                      signature=settings.mail_signature, title=settings.mail_title)
    msg.attach(MIMEText(body.encode("utf-8"), "html", "utf-8"))
        
    try:
        with open(settings.pdf_dir + fname, "rb") as fobj:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(fobj.read())
        
        encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=fname_enc)
        msg.attach(part)
        
        server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
        if settings.smtp_TLS:
            server.starttls()
        server.login(sender_addr, passwd)
        server.sendmail(sender_addr, recipient_addr, msg.as_string())
        server.quit()
        settings.logger.debug("Email has been sent successfully!")
        return 0
    except Exception as e:
        settings.logger.debug("Email cannot be sent")
        settings.logger.error(str(e))
        return 1