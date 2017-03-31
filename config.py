#!/usr/local/bin/python
# -*- coding: utf8 -*-
import os

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ['SECRET_KEY']

CITIES = [
    ('Скопје', 'Скопје'), ('Битола', 'Битола'), ('Прилеп', 'Прилеп'), ('Велес', 'Велес'), ('Тетово', 'Тетово'),
    ('Гостивар', 'Гостивар'),('Куманово', 'Куманово'),('Струмица', 'Струмица'),('Охрид', 'Охрид'), ('Струга', 'Струга'),
    ('Кочани', 'Кочани'), ('Кавадарци', 'Кавадарци'), ('Неготино', 'Неготино'),
    ('Св. Николе', 'Св. Николе'), ('Берово', 'Берово'), ('Виница', 'Виница'), ('Делчево', 'Делчево'),
    ('Мк. Каменица', 'Мк. Каменица'), ('Пехчево', 'Пехчево'), ('Пробиштип', 'Пробиштип'), ('Штип', 'Штип'),
    ('Дебар', 'Дебар'), ('Кичево', 'Кичево'), ('Мк. Брод', 'Мк. Брод'),
    ('Богданци', 'Богданци'), ('Валандово', 'Валандово'), ('Гевгелија', 'Гевгелија'),
    ('Радовиш', 'Радовиш'), ('Демир Хисар', 'Демир Хисар'), ('Крушево', 'Крушево'),
    ('Ресен', 'Ресен'), ('Кратово', 'Кратово'), ('Кр. Паланка', 'Кр. Паланка'), ('Демир Капија', 'Демир Капија'),
]
SK_AREA = [
     ('сите','Сите населби'), ('Центар', 'Центар'), ('Аеродром','Аеродром'), ('Карпош','Карпош'),('Кисела Вода','Кисела Вода'),
     ('Ѓорче Петров', 'Ѓорче Петров'), ('Чаир','Чаир'), ('Бутел','Бутел'), ('Гази Баба','Гази Баба'),
     ('Сарај','Сарај'), ('Шуто Оризари','Шуто Оризари')
]

CONDO_STATUS = [('0', 'Зафатен'), ('1', 'Слободен')]
CONDO_TYPE = [('0', 'Се продава'), ('1', 'Се изнајмува')]

QUADRATURES = []
for i in range(200, 20, -5):
    QUADRATURES.append(str(i))
ROOMS = ['8', '7', '6','5', '4', '3', '2', '1']
FLOOR = []
for i in range(16, -1, -1):
    FLOOR.append(str(i))

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

UPLOAD_FOLDER = 'app/static/img/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'JPG']
MAX_CONTENT_LENGTH = 10 * 1024 * 1024
MAX_PICS = 8

COMMENTS_PER_PAGE = 5
LISTINGS_PER_PAGE = 10

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ['MAIL_USERNAME']
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
ADMIN = 'НајдиСтан.мк'
