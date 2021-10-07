from qbay import app
from flask_sqlalchemy import SQLAlchemy


'''
This file defines data models and related business logics
'''


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    wallet = db.Column(db.Float, nullable=False, default=0.0)
    posts = db.relationship('Post', backref='seller', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.username
        
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Float)
    description = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return '<Review %r>' % self.reviewId
        
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller = db.Column(db.String(25), nullable=False)
    buyer = db.Column(db.String(25), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    
    def __repr__(self):
        return '<Transaction %r>' % self.transactionId

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.postId


# create all tables
db.create_all()


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
    # check if the email has been used:
    existed = User.query.filter_by(email=email).all()
    if len(existed) > 0:
        return False

    # create a new user
    user = User(username=name, email=email, password=password)
    # add it to the current database session
    db.session.add(user)
    # actually save the user object
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
