from flask import render_template, request, session, redirect
from qbay.models import create_product, update_product, login
from qbay.models import User, Product, register, is_float, update_user
from datetime import datetime

from qbay import app


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                user = User.query.filter_by(email=email).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = login(email, password)
    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information 
        between a user's browser and the end server. 
        Typically it is packed and stored in the browser cookies. 
        They will be past along between every request the browser made 
        to this services. Here we store the user object into the 
        session, so we can tell if the client has already login 
        in the following sessions.
        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed')


@app.route('/')
@authenticate
def home(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals

    # some fake product data
    products = Product.query.filter_by(user_email=session['logged_in'])
    return render_template('index.html', user=user, products=products)


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
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
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/create', methods=['GET'])
def create_page_get():
    email = session['logged_in']
    user = User.query.filter_by(email=email).first()
    return render_template('create.html', user=user)


@app.route('/create', methods=['POST'])
def create_page_post():
    email = session['logged_in']
    user = User.query.filter_by(email=email).first()
    
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')

    if not is_float(price):
        return render_template(
            'create.html', 
            user=user, 
            message='Wrong price.'
        )
    
    result = create_product(
        title=title,
        description=description,
        price=float(price),
        last_modified_date=datetime.today().strftime('%Y-%m-%d'),
        owner_email=email
    )

    if not result:
        return render_template(
            'create.html', 
            user=user, 
            message='Product not created.'
        )
    return redirect('/', code=303)


@app.route('/update/<prod_name>', methods=['GET'])
def update_page_get(prod_name):
    product = Product.query.filter_by(title=prod_name).first()
    return render_template('update.html', product=product)


@app.route('/update/<prod_name>', methods=['POST'])
def update_page_post(prod_name):
    product = Product.query.filter_by(title=prod_name).first()

    email = session['logged_in']
    user = User.query.filter_by(email=email).first()
    
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')

    if not is_float(price):
        return render_template(
            'update.html', 
            user=user, 
            product=product,
             message='Wrong price.'
        )

    result = update_product(
        title=prod_name,
        title2=title,
        description=description,
        price=float(price)
    )

    return redirect('/', code=303)


@app.route('/profile', methods=['GET'])
def profile_get():
    if len(session) == 0:
        return redirect('/', code=303)
    email = session['logged_in']
    user = User.query.filter_by(email=email).first()
    return render_template('profile.html', user=user)


@app.route('/profile', methods=['POST'])
def profile_post():
    email = session['logged_in']
    user = User.query.filter_by(email=email).first()

    new_username = request.form.get('username')
    shipping_address = request.form.get('address')
    postal_code = request.form.get('postal')

    update_user(
        username=user.username,
        new_username=new_username,
        shipping_address=shipping_address,
        postal_code=postal_code
    )

    return redirect('/')