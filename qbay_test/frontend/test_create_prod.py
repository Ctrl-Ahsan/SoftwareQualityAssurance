from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User
import time
from random import randint


class FrontEndHomePageTest(BaseCase):

    def test_r4_5(self, *_):
        '''
        Shotgun testing
        Randomly input different prices
        '''

        # open register
        self.open(base_url + '/register')
        self.type('#name', 'upupey')
        self.type('#email', 'upupey@test.com')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        self.click('input[type=\'submit\']')
        time.sleep(2)

        # login
        self.type('#email', 'upupey@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # shotgun
        for i in range(1, 10):
            price = randint(10, 10000)
            self.open(base_url + '/create')
            self.type('#title', 'up' * i)
            self.type('#description', 'upupp' * 6)
            self.type('#price', str(price))
            self.click('input[type=\'submit\']')
            self.open(base_url + '/create')

        # test that it didn't fail
        self.open(base_url)
        self.assert_element('h2')
        self.assert_text('Welcome upupey !', 'h2')


