import asyncio
import aiosqlite3
import aiosmtplib
import json

from more_itertools import chunked
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


MAIL_PARAMS = {
    'TLS': True,
    'host': 'smtp.mailtrap.io',
    'username': 'aba1a44638c6a8',
    'password': '0ebcc9aa6a92cf',
    'port': 587,
    'mailfrom': 'test@example.com'
}

async def db_contacts(loop):
    async with aiosqlite3.connect('contacts.db', loop=loop) as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM contacts;")
            list_contacts = await cur.fetchall()
            return list_contacts

async def sendmail_async(mailto,name,**params):
    mail_params = params.get("mail_params", MAIL_PARAMS)
    msg = MIMEMultipart()
    msg.preamble = "Thanks"
    msg['Subject'] = "Thanks"
    msg['From'] = mail_params.get('mailfrom')
    msg['To'] = mailto
    body = f"Уважаемый {name}! \n" \
           f"Спасибо, что пользуетесь нашим сервисом объявлений."
    msg.attach(MIMEText(body, 'plain'))

    host = mail_params.get('host', 'localhost')
    isSSL = mail_params.get('SSL', False)
    isTLS = mail_params.get('TLS', False)
    port = mail_params.get('port', 465 if isSSL else 25)
    smtp = aiosmtplib.SMTP(hostname=host, port=port, use_tls=isSSL)
    await smtp.connect()
    if isTLS:
        await smtp.starttls()
    if 'username' in mail_params:
        await smtp.login(mail_params['username'], mail_params['password'])
    await smtp.send_message(msg)
    await smtp.quit()


async def main():
    loop = asyncio.get_event_loop()
    list_cont = loop.run_until_complete(db_contacts(loop))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    list_cont = loop.run_until_complete(db_contacts(loop))

    co_list = []
    for id, first_name, last_name, mailto, *other in list_cont:
        co1 = sendmail_async(mailto=mailto, name= f'{first_name} {last_name}')
        co_list.append(co1)
    loop.run_until_complete(asyncio.gather(*co_list))

    loop.close()

    # print(*list_cont, sep='\n')
    # print(len(list_cont))

    # co_list = []
    # for mail in list_cont:
    #     co1 = send_mail_async(to=mail[3],name= f'{mail[1]} {mail[2]}')
    #     co_list.append(co1)
    # loop.run_until_complete(asyncio.gather(*co_list))
    # loop.close()