from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User


class FrontEndHomePageTest(BaseCase):
    '''
    The following code is an output coverage test for creating products.

    Below is the partition & the inputs & outputs with that partition,
    Partition 1:
    Valid title, description, & price
    Should go to homepage

    Partition 2:
    Valid title & description, Non-valid price
    Should display product not created

    Partition 3:
    Valid title & price, Non-valid description
    Should display product not created

    Partition 4:
    Valid title, non-valid description & price
    Should display product not created

    Partition 5:
    Non-valid title, valid description & price
    Should display product not created

    Partition 6:
    Non-valid title & price, valid description
    Should display product not created

    Partition 7:
    Non-valid title & description, valid price
    Should display product not created

    Partition 8:
    Non-valid title, description, & price
    Should display product not created
    '''

    def test_create_p1(self, *_):
        '''
        Partition 1
        Valid title, description, & price
        Should go to homepage
        '''

        # open register page
        self.open(base_url + '/register')
        # fill email and password
        self.type('#email', 'testp1@test.com')
        self.type('#name', 'testp1')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        # click enter button
        self.click('input[type=\'submit\']')

        # open login page
        # fill email and password
        self.type('#email', 'testp1@test.com')
        self.type('#password', '123Ab#')
        # click enter button
        self.click('input[type=\'submit\']')

        # create page
        self.open(base_url + '/create')
        self.type('#title', 'p')
        self.type('#description', 'abcde'*5)
        self.type('#price', '10')
        self.click('input[type=\'submit\']')

        self.assert_element('#p')
        self.assert_text('name: p price: 10.0', '#p')


    def test_create_p2(self, *_):
        '''
        Partition 2
        Valid title & description, Non-valid price
        Should display product not created
        '''

        # open register page
        self.open(base_url + '/register')
        # fill email and password
        self.type('#email', 'testp2@test.com')
        self.type('#name', 'testp2')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        # click enter button
        self.click('input[type=\'submit\']')

        # open login page
        # fill email and password
        self.open(base_url + '/login')
        self.type('#email', 'testp2@test.com')
        self.type('#password', '123Ab#')
        # click enter button
        self.click('input[type=\'submit\']')

        # open create page
        self.open(base_url + '/create')
        self.type('#title', 'p'*2)
        self.type('#description', 'abcde'*5)
        self.type('#price', 'a')
        self.click('input[type=\'submit\']')

        self.assert_element('#message')
        self.assert_text('Product not created.', '#message')

    def test_create_p3(self, *_):
        '''
        Partition 3
        Valid title & price, Non-valid description
        Should display product not created
        '''

        # open register page
        self.open(base_url + '/register')
        # fill email and password
        self.type('#email', 'testp3@test.com')
        self.type('#name', 'testp3')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        # click enter button
        self.click('input[type=\'submit\']')

        # open login page
        # fill email and password
        self.open(base_url + '/login')
        self.type('#email', 'testp3@test.com')
        self.type('#password', '123Ab#')
        # click enter button
        self.click('input[type=\'submit\']')

        # create page
        self.open(base_url + '/create')
        self.type('#title', 'p'*3)
        self.type('#description', 'abcde')
        self.type('#price', '10')
        self.click('input[type=\'submit\']')

        self.assert_element('#message')
        self.assert_text('Product not created.', '#message')

    def test_create_p4(self, *_):
        '''
        Partition 4
        Valid title, non-valid description & price
        Should display product not created
        '''

        # open register page
        self.open(base_url + '/register')
        # fill email and password
        self.type('#email', 'testp4@test.com')
        self.type('#name', 'testp4')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        # click enter button
        self.click('input[type=\'submit\']')

        # open login page
        # fill email and password
        self.open(base_url + '/login')
        self.type('#email', 'testp4@test.com')
        self.type('#password', '123Ab#')
        # click enter button
        self.click('input[type=\'submit\']')

        # create page
        self.open(base_url + '/create')
        self.type('#title', 'p'*4)
        self.type('#description', 'abc')
        self.type('#price', 'a')
        self.click('input[type=\'submit\']')

        self.assert_element('#message')
        self.assert_text('Product not created.', '#message')