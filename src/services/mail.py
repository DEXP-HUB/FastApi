import smtplib

from configparser import ConfigParser

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


config = ConfigParser()
config.read('src\config.ini', encoding='utf-8')
config_mail = dict(config.items('Mail'))


def smtp_settings():
    smtp_server = smtplib.SMTP('smtp.mail.ru', 587)
    smtp_server.starttls()
    smtp_server.login(config_mail['from'], config_mail['password'])

    return smtp_server


def message(addres):
    msg = MIMEMultipart()
    msg['From'] = config_mail['from']
    msg['To'] = addres
    msg['Subject'] = config_mail['name_message']

    msg_text = config_mail['message']
    msg.attach(MIMEText(msg_text, 'plain'))

    return msg


def send_message(addres):
    smtp_server = smtp_settings()
    msg = message(addres=addres)

    smtp_server.sendmail(config_mail['from'], msg['To'], msg.as_string())
    smtp_server.quit()

