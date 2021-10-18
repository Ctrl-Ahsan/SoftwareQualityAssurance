from qbay import *
from qbay.cli import login_page, register_page

def main():
    user = None
    while True:
        if user is None:
            selection = input(
                'Welcome. Please type 1 to login. Or 2 register.\n')
            selection = selection.strip()
            if selection == '1':
                user = login_page()
                if user:
                    print(f'welcome {user.username}')
                    continue
                else:
                    print('login failed')
            elif selection == '2':
                register_page()
        else: 
            selection = input (
                'Please type 1 to go to homepage. Or 2 to update profile.')
            selection = selection.strip()

            if selection == '1':
                # Home page here
                continue
            elif selection == '2':
                # Update profile here
                continue


if __name__ == '__main__':
    main()