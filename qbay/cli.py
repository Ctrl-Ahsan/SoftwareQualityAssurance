from qbay.models import login, register, update_user
from qbay.models import create_product, update_product
from datetime import datetime
import re


def login_page():
    '''
    Initial login page for registered users

    '''
    email = input('Please input email: ')
    password = input('Please input password: ')

    return login(email, password)


def register_page():
    '''
    Registration page for new user with 
    email, username and password inputs.
    '''
    email = input('Please input email: ')
    username = input('Please input username')
    password = input('Please input password: ')
    password_twice = input('Please input the password again: ')

    if password != password_twice:
        print('password entered not the same')
    elif register(username, email, password):
        print('registration succeeded')
    else:
        print('regisration failed.')


def update_user_page(initialuser):
    '''
    User information update page. Can update username, 
    shipping address and postal code
    '''
    username = input("Enter the new username: ")
    shipping_address = input("Enter the new shipping address: ")
    postal_code = input("Enter the new postal code: ")

    if update_user(initialuser, username, shipping_address, postal_code):
        print("User updated succesfully")
    else:
        print("User update failed")


def is_float(string):
    '''
    Checks to see if string input is a float
        Parameters: 
            string : input
        Returns: 
            True if float
    '''
    return bool(re.match(r'[0-9]+(.[0-9]+)?', string))


def create_product_page(user):
    '''
    Product posting creation page
        Parameters: 
        user : product posting user
    '''
    title = input('Enter title: ')
    description = input('Enter description: ')
    price = input('Enter price: ')

    if not is_float(price):
        print('product creation failed.')
        return

    result = create_product(
        title=title,
        description=description,
        price=float(price),
        last_modified_date=datetime.today().strftime('%Y-%m-%d'),
        owner_email=user.email
    )

    if result:
        print('product creation succeeded.')
    else:
        print('product creation failed.')


def update_product_page(user):
    '''
    Update product posting page
        Parameters: 
        user : product posting user
    '''
    number_of_posts = len(user.posts)
    if number_of_posts == 0:
        print('no products to update.')
        return 

    print(f'\n{number_of_posts} Post(s):')
    for i, product in enumerate(user.posts):
        print(f'{i+1}. {product.title}')

    post = input('\nEnter the product number you would like to update.\n')
    post = post.strip()

    if not post.isnumeric():
        print('product update failed.')
        return

    if (int(post) - 1 >= 0 and int(post) - 1 < number_of_posts):
        title = user.posts[int(post) - 1].title
        description = user.posts[int(post) - 1].description
        price = user.posts[int(post) - 1].price

        print('\n1. Update title\n2. Update description\n3. Update price')
        selection = input('\nEnter option number: ')
        selection = selection.strip()

        if selection == '1':
            title = input('Enter new title: ')
        elif selection == '2':
            description = input('Enter new description: ')
        elif selection == '3':
            price = input('Enter a new price: ')

            if not is_float(price):
                print('product update failed.')
                return

        result = update_product(
            user.posts[int(post) - 1].title,
            title,
            description,
            float(price)
        )

        if result:
            print('product update succeeded.')
        else:
            print('product update failed.')

    

