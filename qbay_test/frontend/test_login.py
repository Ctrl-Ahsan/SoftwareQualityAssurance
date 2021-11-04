from seleniumbase import BaseCase
from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User, testing_register


"""
This file defines all integration tests for the frontend homepage. 
"""


class FrontEndHomePageTest(BaseCase):
    def test_login_R2_1_1(self, *_):
        """
        Output coverage testing R2_1 part 1
        Testing for the login succesful output
        """
        testing_register("R2_1_1", "R2_1_1@test.com", "Test123$")
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "R2_1_1@test.com")
        self.type("#password", "Test123$")
        # click enter button
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome R2_1_1 !", "#welcome-header")
        # other available APIs

    def test_login_R2_1_2(self, *_):
        """
        Output coverage testing R2_1 part 2
        Testing for the login failure output
        """
        testing_register("R2_1_2", "R2_1_2@test.com", "Test123$")
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "wrong@test.com")
        self.type("#password", "Wrong123$")
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
        testing_register("R2_2_1", "test", "test")
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test")
        self.type("#password", "test")
        # click enter button
        self.click('input[type="submit"]')

        self.assert_text("login failed", "#message")