import asyncio
import aiosqlite3
import aiosmtplib

from more_itertools import chunked
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MAX_MAILS = 25

MAIL_PARAMS = {
    'host': '127.0.0.1',
    'port': 1025,
    'mailfrom': 'test@example.com'
}


async def db_contacts():
    async with aiosqlite3.connect('contacts.db') as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM contacts;")
            list_contacts = await cur.fetchall()
    return list_contacts


async def sendmail_async(mailto, name, **params):
    mail_params = params.get("mail_params", MAIL_PARAMS)
    msg = MIMEMultipart()
    msg['Subject'] = "Вот спасибки, так спасибки!"
    msg['From'] = mail_params.get('mailfrom')
    msg['To'] = mailto

    body = f'''Уважаемый {name}!
Спасибо, что пользуетесь нашим сервисом объявлений.'''

    msg.attach(MIMEText(body, 'plain'))

    host = mail_params.get('host', 'localhost')
    port = mail_params.get('port')
    smtp = aiosmtplib.SMTP(hostname=host, port=port)
    await smtp.connect()
    result = await smtp.send_message(msg)
    await smtp.quit()
    return result


async def main():
    contacts = await db_contacts()
    for contacts_chunk in chunked(contacts, MAX_MAILS):
        sendmail_coroutines = [
            sendmail_async(mailto=mailto, name=f'{first_name} {last_name}')
            for _, first_name, last_name, mailto, *other in contacts_chunk
        ]
        await asyncio.gather(*sendmail_coroutines)


if __name__ == '__main__':
    asyncio.run(main())
