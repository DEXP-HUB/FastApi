import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def smtp_settings():
    data = data_message()
    
    smtp_server = smtplib.SMTP('smtp.mail.ru', 587)
    smtp_server.starttls()
    smtp_server.login(data['from_mail'], data['my_password'])

    return smtp_server


def message():
    msg = MIMEMultipart()
    msg['From'] = 'ali_guseynov_02@mail.ru'
    msg['To'] = 'gusejnovali508@gmail.com'
    msg['Subject'] = 'Подтверждение регистрации'

    msg_text = 'Спасибо за регистрацию в нашем проекте.'
    msg.attach(MIMEText(msg_text, 'plain'))

    return msg
    

def data_message():
    return {
        'from_mail': 'ali_guseynov_02@mail.ru', 
        'my_password': 'N885Zec2wHBu6v5U2irJ', 
        'to_mail': 'gusejnovali508@gmail.com',
        }


def send_message():
    smtp_server = smtp_settings()
    msg = message()
    data = data_message()

    smtp_server.sendmail(data['from_mail'], data['to_mail'], msg.as_string())
    smtp_server.quit()

send_message()
