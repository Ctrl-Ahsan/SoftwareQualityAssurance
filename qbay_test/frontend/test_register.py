from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User

"""
This file defines all integration tests for the frontend homepage.
"""


class FrontEndHomePageTest(BaseCase):
    test1_2_2_user = User (
        id = 1,
        email = "test122@test.com",
        username = "test",
        password = "Test123$",
        balance = 0,
        shipping_address = "",
        postal_code = "",
        posts = None,
        reviews = None,
    )

    def test_Register_R1_1_1(self, *_):
        """
        Output coverage testing R1_1 part 1
        Testing for the registration succesful output
        """
        # open login page
        self.open(base_url + '/register')
        # fill email and password
        self.type("#email", "test@test.com")
        self.type("#name", "test")
        self.type("#password", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test !", "#welcome-header")
    
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
        # click enter button
        self.click('input[type="submit"]')

        self.assert_text("Registration failed.", "#message")

    def test_Register_R1_2_1(self, *_):
        """
        Input coverage testing R2_1 part 1
        Partition 1: Unique email
        """
        # open login page
        self.open(base_url + '/register')
        # fill email and password
        self.type("#email", "test2@test.com")
        self.type("#name", "test")
        self.type("#password", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test !", "#welcome-header")

    def test_Register_R1_1_2(self, *_):
        """
        Input coverage testing R2_1 part 2
        Partition 2: Email is not unqiue
        """
        # open login page
        self.open(base_url + '/register')
        # fill email and password
        self.type("#email", "test122@test.com")
        self.type("#name", "test")
        self.type("#password", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        self.assert_text("Registration failed.", "#message")
