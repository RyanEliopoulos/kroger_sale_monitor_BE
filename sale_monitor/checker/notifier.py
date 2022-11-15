import smtplib
import os


def send_notification(recipient, message):
    login: str = os.getenv('ip_alert_email')
    password: str = os.getenv('ip_alert_email_pw')
    sm = smtplib.SMTP(host='smtp.gmail.com', port=587)
    sm.starttls()
    sm.login(login, password)
    sm.sendmail(login, recipient, message)