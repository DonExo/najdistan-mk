#!/usr/local/bin/python
# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import BooleanField,StringField, SelectField
from wtforms.fields.simple import PasswordField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from config import CITIES, QUADRATURES, ROOMS, FLOOR, SK_AREA, CONDO_STATUS, CONDO_TYPE


class LoginForm(FlaskForm):
    email = StringField('Е-маил адреса', validators=[DataRequired(message='Задолжително поле'), Length(min=3, message='Е-маилот мора да содржи барем 3 карактери.'), Email(message='Внесете валиден емаил во формат: john@doe.com')])
    password = PasswordField('Лозинка', validators=[DataRequired(message='Задолжително поле'), Length(min=3, max=50,message='Лозинката мора да биде помеѓу 3 и 50 карактери.')])
    remember_me = BooleanField('Зачувај сесија', default=False)

class UserEditProfile(FlaskForm):
    fullName = StringField('Име и презиме', validators=[DataRequired(message='Задолжително поле'), Length(min=3, max=30, message='Името мора да биде помеѓу 3 и 30 карактери.')])
    email = StringField('Е-маил адреса', validators=[DataRequired(message='Задолжително поле'), Length(min=3,message='Е-маилот мора да содржи барем 3 карактери.'),Email(message='Внесете валиден емаил во формат: john@doe.com')])
    password1 = PasswordField('Нова лозинка', validators=[EqualTo('repeatPassword1', message='Лозинките не се совпаѓаат.')])
    repeatPassword1 = PasswordField('Повторно лозинка')
    currentPassword1 = PasswordField('Тековна лозинка', validators=[DataRequired(message='Задолжително поле'), Length(min=3, max=50, message='Лозинката мора да биде помеѓу 3 и 50 карактери.')])
    telNumber = StringField('Број за контакт', validators=[DataRequired(message='Задолжително поле'),Length(min=8, max=30,message='Тел. број мора да биде во формат: 07X/yyy-YYY')])

class RegisterForm(FlaskForm):
    fullName = StringField('Име и презиме', validators=[DataRequired(message='Задолжително поле'), Length(min=3, max=30, message='Името мора да биде помеѓу 3 и 30 карактери.')])
    email = StringField('Е-маил адреса', validators=[DataRequired(message='Задолжително поле'), Length(min=3, message='Е-маилот мора да содржи барем 3 карактери.'), Email(message='Внесете валиден емаил во формат: john@doe.com')])
    password = PasswordField('Лозинка', validators=[DataRequired(message='Задолжително поле'), Length(min=3, max=50, message='Лозинката мора да биде помеѓу 3 и 50 карактери.')])
    repeatPassword = PasswordField('Повторно лозинка', validators=[DataRequired(message='Задолжително поле'), Length(min=3, max=50, message='Лозинката мора да биде помеѓу 3 и 50 карактери.'), EqualTo('password', message="Лозинките не се совпаѓаат")])
    telNumber = StringField('Број за контакт', validators=[DataRequired(message='Задолжително поле'), Length(min=8, max=30, message='Тел. број мора да биде во формат: 07X/yyy-YYY')])
    regIP = StringField('regIp')
    isAdmin = BooleanField('isAdmin', default=False)
    acceptTOS = BooleanField('Се согласувам со условите', default=False)

class ListingForm(FlaskForm):
    title = StringField('Наслов', validators=[DataRequired(message='Задолжително поле'), Length(min=2, max=100, message='Насловот мора да биде од 2 до 100 карактери')])
    description = TextAreaField('Опис')
    city = SelectField('Град', choices=CITIES, default='Скопје')
    area = SelectField('Регион', choices=SK_AREA, default='Центар')
    areas = SelectField('Регион', choices=SK_AREA[1:], default='Центар')
    address = StringField('Адреса')
    quadrature = SelectField('Квадратура', choices=[(q, q) for q in QUADRATURES], default='100')
    rooms = SelectField('Број на соби', choices=[(r, r) for r in ROOMS], default='5')
    floor = SelectField('Кат', choices=[(f, f) for f in FLOOR], default='3')
    price = StringField('Цена во Евра', validators=[DataRequired(message='Задолжително поле'), Length(min=1, max=9, message='Внесете цел број')])
    file = FileField('Прикачи слики', render_kw={"multiple":""}, validators=[DataRequired(message='Задолжително поле')])
    available = SelectField('Статус', choices=[(k, v) for k,v in CONDO_STATUS], default='1')
    condoType = SelectField('Тип на оглас', choices=[(k, v) for k, v in CONDO_TYPE], default='0')

class ListingIndex(FlaskForm):
    city = SelectField('Град', choices=CITIES)
    area = SelectField('Регион', choices=SK_AREA)
    keyword = StringField('Барај по клучен збор')
    types = SelectField('Тип', choices=[('0', 'Се продава'), ('1', 'Се издава')])
    submit = SubmitField('П Р Е Б А Р А Ј')

class CommentaryForm(FlaskForm):
    body = TextAreaField('Вашиот коментар:', validators=[DataRequired(message='Задолжително поле'), Length(min=5, max=150, message='Минимум 5 карактери, максимум 150.')], render_kw={'placeholder':'Пр. Здраво, ме интересира дали станот има подно греење...?'})
    submit = SubmitField('Постирај')

class PassRecoveryForm(FlaskForm):
    email = StringField('Е-маил адреса', validators=[DataRequired(message='Задолжително поле'), Length(min=3,message='Е-маилот мора да содржи барем 3 карактери.'),Email(message='Внесете валиден емаил во формат: john@doe.com')])