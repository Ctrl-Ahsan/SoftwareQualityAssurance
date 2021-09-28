from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    wallet = db.Column(db.Float, nullable=False, default=0.0)
    posts = db.relationships('Post', backref='seller', lazy=True)
    reviews = db.relationships('Review', backref='author', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.username
        
class Review(db.Model):
    reviewId = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Float)
    description = db.Column(db.text, nullable=False)
    
    def __repr__(self):
        return '<Review %r>' % self.reviewId
        
class Transaction(db.Model):
    transactionId = db.Column(db.Integer, primary_key=True)
    seller = db.Column(db.String(25), nullable=False)
    buyer = db.Column(db.String(25), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    
    def __repr__(self):
        return '<Transaction %r>' % self.transactionId