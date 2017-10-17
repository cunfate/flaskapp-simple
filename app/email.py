from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    print(app.config['MAIL_USERNAME'])
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_mail_smtp(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    sender = app.config['MAIL_USERNAME']
    password = app.config['MAIL_PASSWORD']
    print("sender:", sender)
    print("password:", password)
    receiver = to
    message = MIMEText(render_template(template + '.txt', **kwargs),
                       'plain', 'utf-8')
    message['From'] = formataddr(["flaskapp", sender])
    message['To'] = formataddr(['dear', receiver])
    message['Subject'] = subject
    server = None
    try:
        server = smtplib.SMTP("smtp.qq.com")
        sever.connect()
    except Exception as e:
        print("get Exception in email.py, SMTP_SSL", e)
    try:
        server.login(sender, password)
    except Exception as e:
        print("get Exception in email.py", e)
    try:
        server.sendmail(sender, [receiver, ], message.as_string())
    except Exception as e:
        print("get Exception in email.py:45", e)
    server.quit()
