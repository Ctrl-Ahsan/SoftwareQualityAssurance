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
    # posts = db.relationship('Product', backref='creator', lazy=True)
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
    owner_email = db.Column(db.String(120), nullable=False)
    title = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    price = db.Column(db.Float, nullable=False)
    last_modified = db.Column(db.String(10), unique=False, nullable=False)

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


def createProduct(title, description, price, last_modified_date, owner_email):
    # Register a new user
    #   Parameters:
    #     title (string):          prod title
    #     description (string):    prod description
    #     price (double):          prod price
    #     last_modified_date(date):prod last_modified_date
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

    # Check is date is valid
    if not validDate(last_modified_date):
        return False

    # Get prod id
    productCount = db.session.query(Product).count()

    # Create product
    product = Product(
        id=productCount + 1,
        owner_email=owner_email,
        title=title,
        description=description,
        price=price,
        last_modified=last_modified_date
    )

    # Add product, return true
    db.session.add(product)
    db.session.commit()
    return True


def updateProduct(title, title2, description, price):
    # updates a product
    #   Parameters:
    #     title (string):          prod title
    #     title2(string):
    #     description (string):    prod description
    #     price (double):          prod price
    #   Returns:
    #     True if product is succesfully updated otherwise False

    # Check if new title is valid
    if not validTitle(title2):
        return False

    # Check if old product name exists
    titleExisted = Product.query.filter_by(title=title).all()
    if len(titleExisted) == 0:
        return False

    # Check if new product name is uniqe
    titleExists = Product.query.filter_by(title=title2).all()
    if len(titleExists) > 0:
        return False

    # Check if description is valid
    if not validDescription(description, title):
        return False

    # Check if price is valid
    if not validPrice(price):
        return False

    # Query for product
    product = Product.query.filter_by(title=title).first()

    if(product.price > price):
        return False

    product.title = title2
    product.description = description
    product.price = price
    product.last_modified = datetime.today().strftime('%Y-%m-%d')

    db.session.commit
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
    if 20 <= len(description) <= 2000 and len(description) > len(title):
        return True
    return False


def validDate(date):
    # Returns true is date falls in acceptable range
    if date > '2025-01-02' or date < '2021-01-02':
        return False
    return True


def login(email, password):

    # Check login information
    #   Parameters:
    #    email (string):    user email
    #    password (string): user password
    #   Returns:
    #     The user object if login succeeded otherwise None

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


def updateUser(username, new_username, shipping_address, postal_code):
    # Check login information
    # Parameters:
    # update_type (string): user information to be updated
    # ("username", "shipping address", "postal code")
    # name (string): user username
    # update_field (string): updated value
    # Returns:
    # The true if user info update succeeded otherwise None

    if not is_proper_username(new_username):
        return False

    # Check if old username exists
    userExisted = User.query.filter_by(username=username).all()
    if len(userExisted) == 0:
        return False

    # Check if new name is uniqe
    userExists = User.query.filter_by(username=new_username).all()
    if len(userExists) > 0:
        return False

    if not is_proper_shipping_address(shipping_address):
        return False

    if not is_proper_postal_code(postal_code):
        return False

    user = User.query.filter_by(username=name).first()
    user.username = new_username
    user.shipping_address = shipping_address
    user.postal_code = postal_code

    db.session.commit()
    return True


def is_proper_postal_code(postal_code):
    postal_code.replace(" ", "")
    postal_code.upper()
    regex = r'[ABCEGHJKLMNPRSTVXY][0-9][A-Z][0-9][A-Z][0-9]'
    if re.match(regex, postal_code):
        return True
    else:
        return False


def is_proper_shipping_address(address):
    # returns true if shipping address is valid, false otherwise
    address.replace(" ", "")
    if address == "" or not address.isalnum():
        return False
    else:
        return True
