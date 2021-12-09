import re
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import backref
from qbay import app


db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True)
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
    user = db.Column(db.String(320), 
                     db.ForeignKey('user.email'), nullable=False)
    user_email = db.Column(db.String(320), unique=False, nullable=False)
    score = db.Column(db.Integer)
    review = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Review %r>' % self.id


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), unique=False, nullable=False)
    seller_email = db.Column(db.String(320), nullable=False, unique=False)
    buyer_email = db.Column(db.String(320), nullable=False, unique=False)
    product_id = db.Column(db.Integer, unique=True)
    price = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return '<Transaction %r>' % self.id


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(320), 
                           db.ForeignKey('user.email'), nullable=False)
    title = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    price = db.Column(db.Float, nullable=False)
    last_modified = db.Column(db.String(10), unique=False, nullable=False)

    transaction = db.Column(db.Integer, unique=True, default=None)

    def __repr__(self):
        return '<Post %r>' % self.id


db.create_all()


def is_complex_password(password):
    '''
    Checks to see if password given is correct
      Parameters:
        password (string):           password used
      Returns:
        True if correct password is passed otherwise False
    '''
    regex = r'[\s!\"#\$%&\'\(\)\*\+,-\./:;<=>\?@\[\]\^_`\{\|\}~]'
    if not bool(re.search(regex, password)):
        return False
    if not bool(re.search(r'[a-z]', password)):
        return False
    if not bool(re.search(r'[A-Z]', password)):
        return False
    return len(password) >= 6


def is_email(email):
    '''
    Checks to see if email given is correct
      Parameters:
        email (string):           user email
      Returns:
        True if correct email is passed otherwise False
    '''
    regex = (r'([!#-\'*+/-9=?A-Z^-~-]+(\.[!#-\'*+/-9=?A-Z^-~-]+)*|\'"([]!#-[^-'
             r'~\t]|(\\[\t -~]))+")@([!#-\'*+/-9=?A-Z^-~-]+(\.[!#-\'*+/-9=?'
             r'A-Z^-~-]+)*|\[[\t -Z^-~]*])')

    return bool(re.match(regex, email))


def is_proper_username(name):
    '''
    Checks to see if username given is correct
      Parameters:
        name (string):           username
      Returns:
        True if correct username is passed otherwise False
    '''
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


# bypass requirements, used in testing
def bypass_register(name, email, password):
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


def create_product(title, description, price, last_modified_date, owner_email):
    '''
    Create a new product
      Parameters:
        title (string):          prod title
        description (string):    prod description
        price (double):          prod price
        last_modified_date(date):prod last_modified_date
        owner_email (string):    prod owner_email
      Returns:
        True if product is successfully added otherwise False
    '''

    # Check if user exists
    user_exists = User.query.filter_by(email=owner_email).all()
    if len(user_exists) == 0:
        return False

    # Check if title is valid
    if not valid_title(title):
        return False

    # Check if product name is uniqe
    title_exists = Product.query.filter_by(title=title).all()
    if len(title_exists) > 0:
        return False

    # Check if description is valid
    if not valid_description(description, title):
        return False

    # Check if price is valid
    if not valid_price(price):
        return False

    # Check is date is valid
    if not valid_date(last_modified_date):
        return False

    # Get prod id
    product_count = db.session.query(Product).count()

    # Create product
    product = Product(
        id=product_count + 1,
        user_email=owner_email,
        title=title,
        description=description,
        price=price,
        last_modified=last_modified_date
    )

    # Add product, return true
    db.session.add(product)
    db.session.commit()
    return True


def update_product(title, title2, description, price):
    '''
    Updates a product
      Parameters:
        title (string):          prod title
        title2(string):
        description (string):    prod description
        price (double):          prod price
      Returns:
        True if product is successfully updated otherwise False
    '''

    # Check if new title is valid
    if not valid_title(title2):
        return False

    # Check if old product name exists
    title_existed = Product.query.filter_by(title=title).all()
    if len(title_existed) == 0:
        return False

    # Check if new product name is uniqe
    if not title == title2:
        titleExists = Product.query.filter_by(title=title2).all()
        if len(titleExists) > 0:
            return False

    # Check if description is valid
    if not valid_description(description, title):
        return False

    # Check if price is valid
    if not valid_price(price):
        return False

    # Query for product
    product = Product.query.filter_by(title=title).first()

    if(product.price > price):
        return False

    product.title = title2
    product.description = description
    product.price = price
    product.last_modified = datetime.today().strftime('%Y-%m-%d')

    db.session.commit()
    return True


def valid_title(title):
    '''
    Checks to see if title is correct
      Parameters:
        title (string):           title of product
      Returns:
        True if correct title is passed otherwise False
    '''
    if(title[0] == " " or title[-1] == " " or len(title) > 80):
        return False
    if all(x.isalpha() or x.isnumeric() or x.isspace() for x in title):
        return True
    return False


def valid_price(price):
    '''
    Checks to see if price is correct
      Parameters:
        price (float):           price of product
      Returns:
        True if correct price is passed otherwise False
    '''
    if 10.0 <= price <= 10000.0:
        return True
    return False


def valid_description(description, title):
    '''
    Checks to see if description is correct
      Parameters:
        description (string):           description of product
      Returns:
        True if correct description is passed otherwise False
    '''
    if 20 <= len(description) <= 2000 and len(description) > len(title):
        return True
    return False


def valid_date(date):
    '''
    Checks to see if date is correct
      Parameters:
        date (string):           date of product
      Returns:
        True if correct date is passed otherwise False
    '''
    if date > '2025-01-02' or date < '2021-01-02':
        return False
    return True


def login(email, password):
    '''
    Login users
      Parameters:
        email (string):           email of user
        password (string):        email of password
      Returns:
        User account if correct info is passed otherwise None
    '''

    # Perform checks prior to query
    # Check if email is valid
    if not is_email(email):
        return None

    # Check is password is valid
    if not is_complex_password(password):
        return None

    # Find and return the user is they exist
    valids = User.query.filter_by(email=email, password=password).all()
    if len(valids) != 1:
        return None
    return valids[0]


def update_user(username, new_username, shipping_address, postal_code):
    '''
    Updates user profile
      Parameters:
        username (string):           username of user
        new_username (string):       new username of user
        shipping_address (string):   shipping address of user
        postal_code (string):        postal code of user
      Returns:
        True if user profile is updated otherwise False
    '''

    if not is_proper_username(new_username):
        return False

    # Check if old username exists
    user_existed = User.query.filter_by(username=username).all()
    if len(user_existed) == 0:
        return False

    # Check if new name is uniqe
    if not username == new_username:
        user_exists = User.query.filter_by(username=new_username).all()
        if len(user_exists) > 0:
            return False

    if not is_proper_shipping_address(shipping_address):
        return False

    if not is_proper_postal_code(postal_code):
        return False

    user = User.query.filter_by(username=username).first()
    user.username = new_username
    user.shipping_address = shipping_address
    user.postal_code = postal_code

    db.session.commit()
    return True


def is_proper_postal_code(postal_code):
    '''
    Checks postal code
      Parameters:
        postal_code (string):     postal code of user
      Returns:
        True if correct postal code otherwise False
    '''
    regex = r'[ABCEGHJKLMNPRSTVXY][0-9][A-Z][0-9][A-Z][0-9]'
    if re.match(regex, postal_code.upper().replace(" ", "")):
        return True
    else:
        return False


def is_proper_shipping_address(address):
    '''
    Checks shipping address
      Parameters:
        address (string):     address of user
      Returns:
        True if correct address otherwise False
    '''
    address_ns = address.replace(" ", "")
    if address_ns == "" or not address_ns.isalnum():
        return False
    else:
        return True


def is_float(string):
    '''
    Checks to see if string input is a float
        Parameters: 
            string : input
        Returns: 
            True if float
    '''
    return bool(re.match(r'^[0-9]+(.[0-9]+)?$', string))


def buy_product(prod_name, email):
    user = User.query.filter_by(email=email).all()
    product = Product.query.filter_by(title=prod_name).first()
    if product is None or user.balance < product.price:
        return False
    if product.user_email == user.email:
        return False
    if user.shipping_address == '' or user.postal_code == '':
        return False

    user.balance -= product.price

    transaction = Transaction(
        seller_email=product.user_email, 
        buyer_email=user.email,
        product_id=product.id,
        price=product.price,
        date=datetime.today().strftime('%Y-%m-%d')
    )

    db.session.add(transaction)
    db.session.commit()
    print(transaction.id)
    product.transaction = transaction.id
    product.user_email = user.email
    product.last_modified = datetime.today().strftime('%Y-%m-%d')
    db.session.commit()

    print(product.user_email)
    return True