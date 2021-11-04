from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User


#This file defines all integration tests for the frontend homepage.



class FrontEndHomePageTest(BaseCase):

    def test_R4_1(self, *_):
        """
        This is a sample front end unit test to login to home page
        and verify if the tickets are correctly listed.
        """
         #open login page
        self.open(base_url + '/create')
        # fill email and password
        self.type("#title", "Bicycle 2012")
        self.type("#description", "20 charrrrrrrrrrrrrrrrs minimum")
        self.type("#price", "100")
        # click enter button
        self.click('input[type="create"]')
        

        # open home page
        self.open(base_url + '/p')
        # test if the page loads correctly
        self.assert_element('#Bicycle 2012')
        self.assert_text('name: Bicycle 2012 description: 20 charrrrrrrrrrrrrrrrs minimum price: 10.0')


        self.open(base_url + '/create')
        # fill email and password
        self.type("#title", "Bicycle 2012@@")
        self.type("#description", "20 charrrrrrrrrrrrrrrrs minimum")
        self.type("#price", "100")
        # click enter button
        self.click('input[type="create"]')

        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element('#message')
        self.assert_text('Product not created', '#message')
        # other available APIs
