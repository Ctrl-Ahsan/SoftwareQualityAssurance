from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User
import time
from random import randint


class FrontEndHomePageTest(BaseCase):

    def test_r4_1_1(self, *_):
        '''
        Input coverage

        '''
    # open register
        self.open(base_url + '/register')
        self.type('#name', 'upupeyy')
        self.type('#email', 'upupeyy@test.com')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        self.click('input[type=\'submit\']')

        # login
        self.type('#email', 'upupeyy@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # partition 1
        self.open(base_url + '/create')
        self.type('#title', '  prefix space')
        self.type('#description', 'stuff' * 6)
        self.type('#price', '15')
        self.click('input[type=\'submit\']')

        self.assert_element('#message')
        self.assert_text('Product not created.', '#message')

    def test_r4_1_2(self, *_):
        # login
        self.open(base_url + '/login')
        self.type('#email', 'upupeyy@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # partition 2
        self.open(base_url + '/create')
        self.type('#title', 'space at end  ')
        self.type('#description', 'stuffs' * 6)
        self.type('#price', '40')
        self.click('input[type=\'submit\']')

        self.assert_element('#message')
        self.assert_text('Product not created.', '#message')

    def test_r4_1_3(self, *_):
        self.open(base_url + '/login')
        # login
        self.type('#email', 'upupeyy@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # partition 3
        self.open(base_url + '/create')
        self.type('#title', 'not@alpha')
        self.type('#description', 'stuffs' * 6)
        self.type('#price', '25')
        self.click('input[type=\'submit\']')

        self.assert_element('#message')
        self.assert_text('Product not created.', '#message')

    def test_r4_1_4(self, *_):
        self.open(base_url + '/login')

        # login
        self.type('#email', 'upupeyy@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')
        # partition 4
        self.open(base_url + '/create')
        self.type('#title', 'bicycle2012')
        self.type('#description', 'things' * 6)
        self.type('#price', '50')
        self.click('input[type=\'submit\']')

        self.assert_element('#bicycle2012')
        self.assert_text('name: bicycle2012 price: 50.0', '#bicycle2012')

    def test_r4_2(self, *_):
        '''
        output coverage test
        '''

        # open register
        self.open(base_url + '/register')
        self.type('#name', 'upupeyyy')
        self.type('#email', 'upupeyyy@test.com')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        self.click('input[type=\'submit\']')
        time.sleep(2)

        # login
        self.type('#email', 'upupeyyy@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # partition 1
        self.open(base_url + '/create')
        self.type('#title', 'title' * 5)
        self.type('#description', 'stuff' * 5)
        self.type('#price', '180')
        self.click('input[type=\'submit\']')

        self.assert_element('#message')
        self.assert_text('Product not created', '#message')

        self.open(base_url + '/register')
        self.type('#name', 'upupedyy')
        self.type('#email', 'upupedyy@test.com')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        self.click('input[type=\'submit\']')
        time.sleep(2)

        # login
        self.type('#email', 'upupedyy@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # partition 2
        self.open(base_url + '/create')
        self.type('#title', 'titles')
        self.type('#description', 'stuff' * 5)
        self.type('#price', '60')
        self.click('input[type=\'submit\']')

        self.assert_element('#titles')
        self.assert_text('name: titles price: 60.0', '#titles')

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

    def test_r4_6(self, *_):
        '''
        output coverage test
        '''

        # open register
        self.open(base_url + '/register')
        self.type('#name', 'upupeyyyy')
        self.type('#email', 'upupeyyyy@test.com')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        self.click('input[type=\'submit\']')

        # login
        self.type('#email', 'upupeyyyy@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # output coverage
        self.open(base_url + '/create')
        self.type('#title', 'upy')
        self.type('#description', 'stuff' * 5)
        self.type('#price', '50')
        self.click('input[type=\'submit\']')
        # Update Product
        self.open(base_url + '/update/upy')
        self.type('#price', '102')
        self.click('input[type=\'submit\']')
        self.open(base_url + '/update/upy')

        # check for modified date
        self.assert_element('#modified')
