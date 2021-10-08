import re
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from qbay import app


db = SQLAlchemy(app)


class User(db.Model):
    email = db.Column(db.String(320), primary_key=True)
    username = db.Column(db.String(19), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    shipping_address = db.Column(db.Text, nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    posts = db.relationship('Product', backref='creator', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.email


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.email'), nullable=False)
    user_email = db.Column(db.String(320), unique=False, nullable=False)
    score = db.Column(db.Integer)
    review = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return '<Review %r>' % self.id


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_email = db.Column(db.String(320), nullable=False, unique=False)
    seller = db.Column(db.String(19), nullable=False)
    buyer = db.Column(db.String(19), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    product_id = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<Transaction %r>' % self.id


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.email'), nullable=False)
    owner_email = db.Column(db.String(120), nullable=False)
    title = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.id


db.create_all()


def is_complex_password(password):
    if not bool(re.search(r'[\s!\"#\$%&\'\(\)\*\+,-\./:;<=>\?@\[\]\^_`\{\|\}~]', password)):
        return False
    if not bool(re.search(r'[a-z]', password)):
        return False
    if not bool(re.search(r'[A-Z]', password)):
        return False
    return len(password) >= 6


def is_email(email):
    regex = (r'([!#-\'*+/-9=?A-Z^-~-]+(\.[!#-\'*+/-9=?A-Z^-~-]+)*|\'"([]!#-[^-'
    r'~\t]|(\\[\t -~]))+")@([!#-\'*+/-9=?A-Z^-~-]+(\.[!#-\'*+/-9=?A-Z^-~-]+)*'
    r'|\[[\t -Z^-~]*])')
    
    return bool(re.match(regex, email))


def is_proper_username(name):
    if len(name) < 3 or len(name) > 19:
        return False
    return bool(re.match(r'^[A-z0-9]+[A-z0-9 ]*[A-z0-9]+$', name))


def register(name, email, password):
    '''
    Register a new user
      Parameters:
        name (string):     user name
        email (string):    user email
        password (string): user password
      Returns:
        True if registration succeeded otherwise False
    '''

    if not is_email(email):
        return False

    # check if the email has been used:
    existed = User.query.filter_by(email=email).all()
    if len(existed) > 0:
        return False

    if not is_complex_password(password):
        return False

    if not is_proper_username(name):
        return False

    user = User(
        email=email,
        username=name,  
        password=password,
        balance=100.0,
        shipping_address='',
        postal_code=''
    )
    
    db.session.add(user)

    db.session.commit()

    return True


def login(email, password):
    '''
    Check login information
      Parameters:
        email (string):    user email
        password (string): user password
      Returns:
        The user object if login succeeded otherwise None
    '''
    valids = User.query.filter_by(email=email, password=password).all()
    if len(valids) != 1:
        return None
    return valids[0]
