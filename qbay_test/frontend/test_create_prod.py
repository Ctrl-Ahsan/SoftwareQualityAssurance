from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User
import time


class FrontEndHomePageTest(BaseCase):

    def test_r4_5(self, *_):
        # open register
        self.open(base_url + '/register')
        self.type('#name', 'upupey')
        self.type('#email', 'upupey@test.com')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        self.click('input[type=\'submit\']')

        # login
        self.type('#email', 'upupey@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # partition 1
        self.open(base_url + '/create')
        self.type('#title', 'upup')
        self.type('#description', 'upupp' * 6)
        self.type('#price', '-1')
        self.click('input[type=\'submit\']')
       
        self.assert_element('#message')
        self.assert_text('Product not created.', '#message')

        # partition 2
        self.type('#title', 'upup')
        self.type('#description', 'upupp' * 6)
        self.type('#price', '10')
        self.click('input[type=\'submit\']')

        self.assert_element('#upup')
        self.assert_text('name: upup price: 10.0', '#upup')

