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
    owner_email = db.Column(db.Integer, db.ForeignKey('user.email'), nullable=False)
    title = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id


db.create_all()


def is_complex_password(password):
    regex = r'[\s!\"#\$%&\'\(\)\*\+,-\./:;<=>\?@\[\]\^_`\{\|\}~]'
    if not bool(re.search(regex, password)):
        return False
    if not bool(re.search(r'[a-z]', password)):
        return False
    if not bool(re.search(r'[A-Z]', password)):
        return False
    return len(password) >= 6


def is_email(email):
    regex = (r'([!#-\'*+/-9=?A-Z^-~-]+(\.[!#-\'*+/-9=?A-Z^-~-]+)*|\'"([]!#-[^-'
             r'~\t]|(\\[\t -~]))+")@([!#-\'*+/-9=?A-Z^-~-]+(\.[!#-\'*+/-9=?'
             r'A-Z^-~-]+)*|\[[\t -Z^-~]*])')
    
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


def createProduct(title, description, price, owner_email):
    # Register a new user
    #   Parameters:
    #     title (string):          prod title
    #     description (string):    prod description
    #     price (double):          prod price
    #     owner_email (string):    prod owner_email
    #   Returns:
    #     True if product is succesfully added otherwise False

    # Check if user exists
    userExists = User.query.filter_by(email=owner_email).all()
    if len(userExists) == 0:
        return False

    # Check if title is valid
    if not validTitle(title):
        return False

    # Check if product name is uniqe
    titleExists = Product.query.filter_by(title=title).all()
    if len(titleExists) > 0:
        return False

    # Check if description is valid
    if not validDescription(description, title):
        return False

    # Check if price is valid
    if not validPrice(price):
        return False

    # Get current date
    lastModified = datetime.today()

    # Get prod id
    productCount = Product.query(Product.id).count()

    # Create product
    product = Product(
        id=productCount + 1,
        owner_email=owner_email,
        title=title,
        description=description,
        price=price,
        last_modified=lastModified
    ) 

    # Add product, return true
    db.session.add(product)
    db.session.commit()
    return True


def validTitle(title):
    # Returns true is the title is alphanumerical, 80 or less characters
    # and has no spaces at beginning or end
    if(title[0] == " " or title[-1] == " " or len(title) > 80):
        return False
    if all(x.isalpha() or x.isnumeric() or x.isspace() for x in title):
        return True
    return False


def validPrice(price):
    # Returns true if price falls in acceptable range
    if 10 <= price <= 10000:
        return True
    return False


def validDescription(description, title):
    # Returns true is description length is acceptable
    if 20 <= len(description) < 2000 and len(description) > len(title):
        return True
    return False


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
