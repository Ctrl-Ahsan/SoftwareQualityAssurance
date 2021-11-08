from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User
import time
from random import randint


class FrontEndHomePageTest(BaseCase):

    def test_r4_3(self, *_):
        '''
        Boundary testing.
        '''
        
        # open register page
        self.open(base_url + '/register')
        self.type('#email', 'lego@test.com')
        self.type('#name', 'leggo')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        self.click('input[type=\'submit\']')

        # open login
        self.type('#email', 'lego@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # partition 1
        self.open(base_url + '/create')
        self.type('#title', 'testing')
        self.type('#description', '123456789abcdefghij')
        self.type('#price', '10')
        self.click('input[type=\'submit\']')
        self.assert_element('#message')
        self.assert_text('Product not created.')

        # partition 2
        self.open(base_url + '/create')
        self.type('#title', 'testing2')
        self.type('#description', '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')
        self.type('#price', '10')
        self.click('input[type=\'submit\']')
        self.assert_element('#message')
        self.assert_text('Product not created.')

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



