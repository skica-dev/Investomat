"""
notyfing user
Currently supports:
- sending email
TODO:
- pushbullet
- SMS
"""
import smtplib
from email.mime.text import MIMEText


def send_email(subject, receipent, content, login, password, server, sender):
    """
    email sending
    """
    mail = 'From: %s\nSubject: %s\n%s' % (sender, subject, content)
    s = smtplib.SMTP(host=server, port=587)
    s.starttls()
    s.login(login, password)
    s.sendmail(sender, receipent, mail)
    s.quit()
    return True
