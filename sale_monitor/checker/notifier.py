import smtplib
import os
import log


def send_notification(recipient, message):
    login: str = os.getenv('ip_alert_email')
    password: str = os.getenv('ip_alert_email_pw')
    sm = smtplib.SMTP(host='smtp.gmail.com', port=587)
    sm.starttls()
    sm.login(login, password)
    ascii_only = message.encode('ascii', 'ignore')
    try:
        sm.sendmail(login, recipient, ascii_only)
    except Exception as e:
        log.log(f'Exception occurred trying to send alert: {e}')
