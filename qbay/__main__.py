from qbay import *
from qbay.cli import login_page, register_page, update_user_page
from qbay.cli import create_product_page, update_product_page


def main():
    user = None
    while True:
        if user is None:
            selection = input(
                'Welcome. Please type 1 to login\n Type 2 for register\n'
                'Any other inputs will exit\n')
            selection = selection.strip()
            if selection == '1':
                user = login_page()
                if user:
                    print(f'welcome {user.username}')
                    continue
                else:
                    print('login failed')
            elif selection == '2':
                user = register_page()
            else:
                break
        else: 
            while True:
                selection = input(
                    'Type 1 to logout and return to the main menu\n'
                    'Type 2 to update profile\n'
                    'Type 3 to create a product\n'
                    'Type 4 to update a product\n')
                selection = selection.strip()

                if selection == '1':
                    user = None
                    break
                elif selection == '2':
                    update_user_page(user.username)
                elif selection == '3':
                    create_product_page(user)
                elif selection == '4':
                    update_product_page(user)
                else:
                    print("Invalid input")


if __name__ == '__main__':
    main()