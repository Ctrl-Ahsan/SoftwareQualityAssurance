from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User, is_complex_password

from random import randrange
from string import ascii_letters, digits, punctuation
import time
import random

"""
This file defines all integration tests for the frontend homepage.
"""


class FrontEndHomePageTest(BaseCase):
    def test_Register_R1_1_1(self, *_):
        """
        Output coverage testing R1_1 part 1
        Testing for the registration succesful output
        """
        # open login page
        self.open(base_url + '/register')
        # fill email and password
        self.type("#email", "R1_1_1@test.com")
        self.type("#name", "R1_1_1")
        self.type("#password", "Test123$")
        self.type("#password2", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        # open login page
        self.open(base_url + "/login")

        # fill email and password
        self.type("#email", "R1_1_1@test.com")
        self.type("#password", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome R1_1_1 !", "#welcome-header")
    
    def test_Register_R1_1_2(self, *_):
        """
        Output coverage testing R1_1 part 2
        Testing for the registration failure output with empty email/password
        """
        # open login page
        self.open(base_url + '/register')
        # fill email and password
        self.type("#email", "")
        self.type("#name", "test")
        self.type("#password", "")
        self.type("#password2", "")
        # click enter button
        self.click('input[type="submit"]')

        self.assert_element_not_visible("#message")

    def test_Register_R1_2_1(self, *_):
        """
        Input coverage testing R1_2 part 1
        Partition 1: Unique email
        """
        # open login page
        self.open(base_url + '/register')
        # fill email and password
        self.type("#email", "R1_2_1@test.com")
        self.type("#name", "R1_2_1")
        self.type("#password", "Test123$")
        self.type("#password2", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        # open login page
        self.open(base_url + "/login")

        # fill email and password
        self.type("#email", "R1_2_1@test.com")
        self.type("#password", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome R1_2_1 !", "#welcome-header")

    def test_Register_R1_2_2(self, *_):
        """
        Input coverage testing R1_2 part 2
        Partition 2: Email is not unqiue
        """
        # open login page
        self.open(base_url + '/register')
        # fill email and password
        self.type("#email", "R1_2_1@test.com")
        self.type("#name", "R1_2_1")
        self.type("#password", "Test123$")
        self.type("#password2", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        self.assert_text("Registration failed.", "#message")

    def test_Register_R1_3_1(self, *_):
        """
        Input coverage testing R1_3 part 1
        Partition 1: Email is constructed properly
        """
        # open login page
        self.open(base_url + '/register')
        # fill email and password
        self.type("#email", "R1_3_1@test.com")
        self.type("#name", "R1_3_1")
        self.type("#password", "Test123$")
        self.type("#password2", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        # open login page
        self.open(base_url + "/login")

        # fill email and password
        self.type("#email", "R1_3_1@test.com")
        self.type("#password", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome R1_3_1 !", "#welcome-header")

    def test_Register_R1_3_2(self, *_):
        """
        Input coverage testing R1_3 part 2
        Partition 2: Email does not follow addr-spec
        """
        # open login page
        self.open(base_url + '/register')
        # fill email and password
        self.type("#email", "R1_3_2testcom")
        self.type("#name", "R1_3_2")
        self.type("#password", "Test123$")
        self.type("#password2", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        self.assert_text("Registration failed.", "#message")

    def test_Register_R1_4_1(self, *_):
        """
        Shotgun testing
        Inputting random passwords to see if registration is succesful
        """
        x = 0
        # Adjust this for number of tested passwords
        while(x < 10):
            x += 1
            username = "R1_4_1" + "_" + str(x)
            email = username + "@test.com"

            randlength = randrange(70)

            characters = ascii_letters + digits + punctuation
            password = ''
            
            for i in range(randlength):
                password = password + random.choice(characters)

            # open login page
            self.open(base_url + '/register')
            # fill email and password

            # fill email and password
            self.type("#email", email)
            self.type("#name", username)
            self.type("#password", password)
            self.type("#password2", password)
            # click enter button
            self.click('input[type="submit"]')

            if(is_complex_password(password)):
                # open login page
                self.open(base_url + "/login")
                # fill email and password
                self.type("#email", email)
                self.type("#password", password)
                # click enter button
                self.click('input[type="submit"]')

                # test if the page loads correctly
                self.assert_element("#welcome-header")
                self.assert_text("Welcome " + username + 
                                 " !", "#welcome-header")
            else:
                self.assert_text("Registration failed.", "#message")
            self.open(base_url + '/logout')

    def test_Register_R1_5_1(self, *_):
        """
        Output coverage testing R1_5 part 1
        Succesful registration output with well constructed username
        """
        # open login page
        self.open(base_url + '/register')
        # fill email and password
        self.type("#email", "R1_5_1@test.com")
        self.type("#name", "R1_5_1")
        self.type("#password", "Test123$")
        self.type("#password2", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        # open login page
        self.open(base_url + "/login")

        # fill email and password
        self.type("#email", "R1_5_1@test.com")
        self.type("#password", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome R1_5_1 !", "#welcome-header")

    def test_Register_R1_5_2(self, *_):
        """
        Output coverage testing R1_5 part 2
        Failed registration output with invalid username
        """
        # open login page
        self.open(base_url + '/register')
        # fill email and password
        self.type("#email", "R1_5_2@test.com")
        self.type("#name", " R1_5_2 ")
        self.type("#password", "Test123$")
        self.type("#password2", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        self.assert_text("Registration failed.", "#message")