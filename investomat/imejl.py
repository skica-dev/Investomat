"""
Module for email sending
"""
import smtplib
from datetime import datetime
from email.mime.text import MIMEText


def send_email(subject, receipent, content, login, password, server, sender):
    """
    sending emails
    """
    mejl = 'From: %s\nSubject: %s\n%s' % (sender, subject, content)
    s = smtplib.SMTP(host=server, port=587)
    s.starttls()
    s.login(login, password)
    s.sendmail(sender, receipent, mejl)
    s.quit()
    return ("sent!")
