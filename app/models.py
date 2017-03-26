#!/usr/local/bin/python
# coding: utf-8

from app import db
import datetime
from hashlib import md5

class Users(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(100), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(32))
    telNumber = db.Column(db.String(30))
    regIP = db.Column(db.String(20))
    regDate = db.Column(db.DateTime)
    lastSeen = db.Column(db.DateTime)
    isAdmin = db.Column(db.Boolean, default=False)
    interestedIn = db.Column(db.String(120))
    condosOwned = db.relationship('Condo', backref='condoOwner', lazy='dynamic')
    commentsOwned = db.relationship('Comment', backref='commentOwner', lazy='dynamic')
    reportedUser = db.relationship('Reports', backref='userReported', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        admins = Users.query.filter(Users.isAdmin == 1).all()
        if self in admins:
            return True
        else:
            return False

    def get_id(self):
        return str(self.userId)

    def __repr__(self):
        return '<User: %r - %r>' % (self.fullName, self.email)

    def __init__(self, fullName, email, password, telNumber, regIP, isAdmin=False):
        self.fullName = fullName
        self.email = email
        self.password = password
        self.telNumber = telNumber
        self.regIP = regIP
        self.regDate = datetime.datetime.utcnow()
        self.lastSeen = datetime.datetime.utcnow()
        self.isAdmin = isAdmin
        self.interestedIn = '0-'

    def avatar(self, size):
        return 'https://www.gravatar.com/avatar/%s?d=wavatar&s=%d&' % (md5(self.email.lower().encode('utf-8')).hexdigest(), size)

class Condo(db.Model):
    condoId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(150))
    city = db.Column(db.String(30))
    area = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(80))
    price = db.Column(db.Integer)
    quadrature = db.Column(db.Integer)
    rooms = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    timesVisited = db.Column(db.Integer)
    available = db.Column(db.Boolean, default=True)
    isApproved = db.Column(db.Boolean, default=False)
    types = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userId'))
    comsPerCondo = db.relationship('Comment', backref='commentsPerCondo', lazy='dynamic')
    imgsPerCondo = db.relationship('Images', backref='imagesPerCondo', lazy='dynamic')
    actedOn = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Condo: %r - %r>' % (self.title, self.price)

    def __init__(self, title, description, city, address, user_id, types, quadrature=0, rooms=0, floor=0, price=0, area=''):
        self.title = title
        self.description = description
        self.city = city
        self.area = area
        self.address = address
        self.quadrature = quadrature
        self.rooms = rooms
        self.floor = floor
        self.price = price
        self.timestamp = datetime.datetime.utcnow()
        self.user_id = user_id
        self.isApproved = False
        self.actedOn = False
        self.types = types
        self.timesVisited = 0

class Comment(db.Model):
    commendId = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    commTimeStamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userId'))
    condo_id = db.Column(db.Integer, db.ForeignKey('condo.condoId'))

    def __repr__(self):
        return '<Comment: %r - %r - %r>' % (self.commendId, self.body, self.condo_id)

    def __init__(self, body, user_id, condo_id):
        self.body = body
        self.commTimeStamp = datetime.datetime.utcnow()
        self.user_id = user_id
        self.condo_id = condo_id

class Images(db.Model):
    imgId = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(256))
    condo_id = db.Column(db.Integer, db.ForeignKey('condo.condoId'))

    def __repr__(self):
        return '<Image: %r - apt:# %r>' % (self.path, self.condo_id)

    def __init__(self, path, condo_id):
        self.path = path
        self.condo_id = condo_id

class Reports(db.Model):
    reportId = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    reason = db.Column(db.String(256))
    condo_id = db.Column(db.Integer, db.ForeignKey('condo.condoId'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.commendId'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.userId'))
    timestamp = db.Column(db.DateTime)
    actedOn = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Report: %r - %r - %r>' % (self.reportId, self.comment_id, self.reason)

    def __init__(self, body, reason, condo_id, comment_id, user_id):
        self.body = body
        self.reason = reason
        self.condo_id = condo_id
        self.comment_id = comment_id
        self.timestamp = datetime.datetime.utcnow()
        self.actedOn = 0
        self.user_id = user_id












