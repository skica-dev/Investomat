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


def send_email(subject, receipent, content, login, password, server):
    """
    email sending
    """
    try:
        mail = 'From: %s\nSubject: %s\n%s' % (login, subject, content)
        s = smtplib.SMTP(host=server, port=587)
        s.starttls()
        s.login(login, password)
        s.sendmail(login, receipent, mail)
        s.quit()
    except:
        raise SendingEmailFailed

    return True
