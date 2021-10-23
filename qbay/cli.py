from qbay.models import login, register, update_user, create_product, update_product
from datetime import datetime


def login_page():
    email = input('Please input email: ')
    password = input('Please input password: ')

    return login(email, password)


def register_page():
    email = input('Please input email: ')
    password = input('Please input password: ')
    password_twice = input('Please input the password again: ')

    if password != password_twice:
        print('password entered not the same')
    elif register('default name', email, password):
        print('registration succeeded')
    else:
        print('regisration failed.')


def update_user_page(initialuser):
    username = input("Enter the new username: ")
    shipping_address = input("Enter the new shipping address: ")
    postal_code = input("Enter the new postal code: ")

    if update_user(initialuser, username, shipping_address, postal_code):
        print("User updated succesfully")
    else:
        print("User update failed")


def create_product_page():
    title = input("Enter the product's title")
    description = input("Enter the product's description")
    price = input("Enter the product's price")
    last_modified_date = datetime.today().strftime('%Y-%m-%d')
    owner_email = input("Enter your email")
    
    if create_product(title, description, price, last_modified_date, owner_email):
        print("Product created succesfully")
    else:
        print("Product creation failed")


def update_product_page():
    initialtitle = input("Enter the title of the product you want to update")
    title = input("Enter the product's new title")
    description = input("Enter the product's new description")
    price = input("Enter the product's new price")

    if update_product(initialtitle, title, description, price):
        print("Product updated succesfully")
    else:
        print("Product updated filed")
    

