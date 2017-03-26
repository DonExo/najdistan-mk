#!/usr/local/bin/python
# coding: utf-8

from flask import render_template
from flask_mail import Message
from threading import Thread
from app import mail, app
from config import ADMIN


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

def emailNotifComment(condoOwner, condo):
    send_email("Некој_коментираше_на_вашиот_оглас!",
               ADMIN, [condoOwner.email],
               "Добивте меил за вашиот оглас на НајдиСтан.мк - Проверете!",
               render_template('emails/emailNotif-comment.html', cid=condoOwner, condo=condo))

def emailNotifRegister(cuser):
    send_email("Успешна_регистрација!",
               ADMIN, [cuser.email],
               "Здраво %s, Ви бладариме што се регистриравте на нашиот систем" % cuser.fullName,
               render_template('emails/emailNotif-register.html', cuser=cuser, ))

def emailNotifPassRecovery(user, newPass):
    send_email('Нова_лозинка!',
               ADMIN, [user.email],
               "Здраво %s, Вашата нова лозинка е: <b>%s</b>" % (user.fullName, newPass),
               render_template('emails/emailNotif-passRecovery.html', user=user, newPass=newPass, ))

def emailNotifCondoMetCriteria(user, condoID):
    send_email('Нов_стан_кој_ги_исполнува_вашите_преференци!',
               ADMIN, [user.email],
               "Здраво %s, објавен е нов стан кој ги исполнува вашите лични преференци!" % user.fullName,
               render_template('emails/emailNotif-CondoMetCriteria.html', user=user, condoID=condoID, ))

def adminMailSend(address, subject, body):
    send_email(subject, ADMIN, [address], body, body)