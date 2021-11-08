from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User
import time
from random import randint


class FrontEndHomePageTest(BaseCase):

    def test_r4_4(self, *_):
        # open register page
        self.open(base_url + '/register')
        self.type('#email', 'short@test.com')
        self.type('#name', 'short')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        self.click('input[type=\'submit\']')

        # open login
        self.type('#email', 'short@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # partition 1
        self.open(base_url + '/create')
        self.type('#title', 'temp')
        self.type('#description', 'tempatempatempatempatempa')
        self.type('#price', '10')
        self.click('input[type=\'submit\']')
        self.assert_element('#temp')
        self.assert_text('name: temp price: 10.0')

        # partition 2
        self.open(base_url + '/create')
        self.type('#title', 'temptemptemptemptemptemptemptemp')
        self.type('#description', 'tempatempatempatempatempa')
        self.type('#price', '10')
        self.click('input[type=\'submit\']')
        self.assert_element('#message')
        self.assert_text('Product not created.')
    
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
    
    def test_r4_8(self, *_):
        # open register page
        self.open(base_url + '/register')
        self.type('#email', 'sametitle@test.com')
        self.type('#name', 'same')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        self.click('input[type=\'submit\']')

        self.type('#email', 'sametitle@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # partition 1
        self.open(base_url + '/create')
        self.type('#title', 'abcb')
        self.type('#description', 'abcbbabcbbabcbbabcbbabcbbabcbb')
        self.type('#price', 10)
        self.click('input[type=\'submit\']')

        self.assert_element('#abcb')
        self.assert_text('name: abcb price: 10.0')

        # partition 2
        self.open(base_url + '/create')
        self.type('#title', 'abcb')
        self.type('#description', 'abcbbabcbbabcbbabcbbabcbbabcbb')
        self.type('#price', 10)
        self.click('input[type=\'submit\']')

        self.assert_element('#message')
        self.assert_text('Product not created', '#message')



