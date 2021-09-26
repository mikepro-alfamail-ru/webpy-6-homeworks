import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery.result import AsyncResult
from app import celery
from celery.contrib import rdb


def sendmail(mailto):
    mail_params = {
        'host': '127.0.0.1',
        'port': 1025,
        'from': 'test@example.com'
    }

    msg = MIMEMultipart()
    msg['Subject'] = "Test message"
    msg['From'] = mail_params.get('from')
    msg['To'] = mailto

    body = 'This is a test message =)'

    msg.attach(MIMEText(body, 'plain'))

    host = mail_params.get('host', 'localhost')
    port = mail_params.get('port')
    smtp = smtplib.SMTP(host=host, port=port)
    result = smtp.send_message(msg)
    return result


@celery.task()
def sendmail_to_users(emails):
    rdb.set_trace()
    for email in emails:
        print(email)
        sendmail(email)


def get_result(task_id):
    task = AsyncResult(task_id, app=celery)
    return task.status, task.result
