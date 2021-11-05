from flask import render_template, request, session, redirect
from qbay.models import create_product, update_product, login
from qbay.models import User, Product, register, is_float, update_user
from flask_login import login_user, login_required, logout_user, current_user
from flask_login import LoginManager
from datetime import datetime

from qbay import app

from sqlalchemy.inspection import inspect

login_manager = LoginManager()
login_manager.login_view = 'login_get'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = login(email, password)
    if user:
        login_user(user, remember=True)
        return redirect('/', code=303)
    else:
        return render_template(
            'login.html', 
            user=current_user, 
            message='login failed'
        )


@app.route('/', methods=['GET'])
@login_required
def home():
    products = Product.query.filter_by(user_email=current_user.email)
    return render_template('index.html', user=current_user, products=products)


@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"
    else:
        # use backend api to register the user
        success = register(name, email, password)
        if not success:
            error_message = 'Registration failed.'
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/create', methods=['GET'])
@login_required
def create_page_get():
    return render_template('create.html', user=current_user)


@app.route('/create', methods=['POST'])
@login_required
def create_page_post():
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')

    if not is_float(price):
        return render_template(
            'create.html', 
            user=current_user, 
            message='Product not created.'
        )
    
    result = create_product(
        title=title,
        description=description,
        price=float(price),
        last_modified_date=datetime.today().strftime('%Y-%m-%d'),
        owner_email=current_user.email
    )

    if not result:
        return render_template(
            'create.html', 
            user=current_user, 
            message='Product not created.'
        )
    return redirect('/', code=303)


@app.route('/update/<prod_name>', methods=['GET'])
@login_required
def update_page_get(prod_name):
    product = Product.query.filter_by(title=prod_name).first()
    if not product:
        return redirect('/')
    return render_template('update.html', product=product)


@app.route('/update/<prod_name>', methods=['POST'])
@login_required
def update_page_post(prod_name):
    product = Product.query.filter_by(title=prod_name).first()

    if not product:
        return redirect('/')
    
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')

    if not is_float(price):
        return render_template(
            'update.html', 
            user=current_user, 
            product=product,
            message='Product not updated.'
        )

    result = update_product(
        title=prod_name,
        title2=title,
        description=description,
        price=float(price)
    )

    if not result:
        return render_template(
            'update.html', 
            user=current_user, 
            product=product,
            message='Product not updated.'
        )

    return redirect('/', code=303)


@app.route('/profile', methods=['GET'])
@login_required
def profile_get():
    return render_template('profile.html', user=current_user)


@app.route('/profile', methods=['POST'])
@login_required
def profile_post():
    new_username = request.form.get('username')
    shipping_address = request.form.get('address')
    postal_code = request.form.get('postal')

    result = update_user(
        username=current_user.username,
        new_username=new_username,
        shipping_address=shipping_address,
        postal_code=postal_code
    )
    
    if not result:
        return render_template(
            'profile.html', 
            user=current_user,
            message='Profile not updated.'
        )

    return redirect('/')