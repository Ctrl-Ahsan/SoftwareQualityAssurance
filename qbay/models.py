import re
from datetime import datetime
from string import ascii_letters, digits
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


def updateUser(update_type, name, update_field)
    '''
    Check login information
      Parameters:
        update_type (string): user information to be updated ("username", "shipping address", "postal code")
        name (string): user username
        update_field (string): updated value
      Returns:
        The true if user info update succeeded otherwise None
    '''
    if(updateType.upper() == "USERNAME" )
        updateUserName(name, update_field)
        return true
    elif(updateType.upper() == "SHIPPING ADDRESS")
        updateShippingAddress(name, update_field)
        return true
    elif(updateType.upper() == "POSTAL CODE")
        updatePostalCode(name, update_field)
        return true
    else
        return None



def updateShippingAddress(name, address)
    #Updates user shipping address using name to search user
    user = User.query.filter_by(username=name)
    if is_proper_shipping_address(address):
        user.shipping_address = address 
        session.commit() 


def updateUserName(prev_username, new_username)
    #Updates username using previous username to search user
    user = User.query.filter_by(username=prev_username)
    if is_proper_username(new_username):
        user.name = new_username
        session.commit() 


def updatePostalCode(name, new_postal_code)
    #Updates user postal code using name to search user
    user = User.query.filter_by(username=name)
    if is_proper_postalCode(new_postal_code):
        user.postal_code = new_postal_code
        session.commit()
        

def is_proper_postalCode(postal_code):
    #returns true if postal code is a valid canadian postal code, false otherwise
    postal_code = postal_code.upper().replace(" ", "")
    if len(postal_code) == 6:
        for i in range(len(postal_code)):
            if i % 2 == 0:
                if i == 0  && not(postal_code[i].isalpha()) && not(postal_code[i] not in ('Y','Z','D','F','I','O','Q','U')):
                    return False 
                elif not(postal_code[i].isalpha())
                    return False
            else:
                if not(postal_code[i].isdigit()) && not (0 < postal_code[i] <=9 ):
                    return False
    else:
        return False
    return postal_code


def is_proper_shipping_address(address):
    #returns true if shipping address is valid, false otherwise
    if address == "" || set(address).difference(ascii_letters + digits):
        return false
    else:
        return true
    
        

