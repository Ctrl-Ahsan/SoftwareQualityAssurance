from qbay import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    shipping_address = db.Column(db.Text, nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    posts = db.relationship('Product', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.username


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_email = db.Column(db.String(25), unique=False, nullable=False)
    score = db.Column(db.Integer)
    review = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return '<Review %r>' % self.id


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_email = db.Column(db.String(120), nullable=False, unique=False)
    seller = db.Column(db.String(25), nullable=False)
    buyer = db.Column(db.String(25), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    product_id = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Transaction %r>' % self.id


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner_email = db.Column(db.String(120), nullable=False)
    title = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.id


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
