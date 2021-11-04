from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User

"""
This file defines all integration tests for the frontend homepage.
"""


class FrontEndHomePageTest(BaseCase):
    test_user = User (
        id = 1,
        email = "test@test.com",
        username = "test",
        password = "Test123$",
        balance = 0,
        shipping_address = "",
        postal_code = "",
        posts = [],
        reviews = [],
    )

    test_user2 = User (
        id = 2,
        email = "test",
        username = "test2",
        password = "test",
        balance = 0,
        shipping_address = "",
        postal_code = "",
        posts = [],
        reviews = [],
    )

    def test_login_R2_1_1(self, *_):
        """
        Output coverage testing R2_1 part 1
        Testing for the login succesful output
        """
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test@test.com")
        self.type("#password", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test !", "#welcome-header")
        # other available APIs

    def test_login_R2_1_2(self, *_):
        """
        Output coverage testing R2_1 part 2
        Testing for the login failure output
        """
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test@test.com")
        self.type("#password", "Test")
        # click enter button
        self.click('input[type="submit"]')

        self.assert_text("login failed", "#message")

    def test_login_R2_2_1(self, *_):
        """
        Input coverage testing R2_2 part 1
        Testing for partition 1: Invalid inputs
        To confirm test_user2 was made with invalid inputs
        login will be attempted with invalid inputs
        as inputs are invalid the database will never be queried
        and login will fail even though user does exist
        """
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test")
        self.type("#password", "test")
        # click enter button
        self.click('input[type="submit"]')

        self.assert_text("login failed", "#message")