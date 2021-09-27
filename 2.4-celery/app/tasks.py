import aiosmtplib
import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery.result import AsyncResult
from app import celery


def sendmail(mailto):
    mail_params = {
        'host': 'mailhog',
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
async def sendmail_async(mailto):
    mail_params = {
        'host': 'mailhog',
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
    smtp = aiosmtplib.SMTP(hostname=host, port=port)
    result = await smtp.send_message(msg)
    return result


async def sendmail_to_users_async(emails):
    sendmail_coroutines = [sendmail_async(email) for email in emails]
    await asyncio.gather(*sendmail_coroutines)


@celery.task()
def sendmail_to_users(emails):
    asyncio.run(sendmail_to_users_async(emails))

def get_result(task_id):
    task = AsyncResult(task_id, app=celery)
    return task.status, task.result
