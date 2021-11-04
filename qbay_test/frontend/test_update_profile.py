from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User


class FrontEndHomePageTest(BaseCase):
    '''
    The following code is functionality tests based off of the specifications.

    Partition 1:
    Update all

    Partition 2:
    Update address

    Partition 3:
    Update postal code

    Partition 4:
    Update username
    '''
    def test_profile_p1(self, *_):
        '''
        Partition 1
        Update all
        '''

        # open register page
        self.open(base_url + '/register')
        self.type('#email', 'profile@test.com')
        self.type('#name', 'profile')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        self.click('input[type=\'submit\']')

        # login
        self.type('#email', 'profile@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # update profile
        self.open(base_url + '/profile')
        self.type('#username', 'profile11')
        self.type('#address', '2 Pancake St')
        self.type('#postal', 'E2E2E2')
        self.click('input[type=\'submit\']')

        # check that it worked
        self.assert_element('#welcome-header')
        self.assert_text('Welcome profile11 !', '#welcome-header')


    # def test_profile_p2(self, *_): 
    #     '''
    #     Partition 2
    #     Update address
    #     '''
    #     # login
    #     self.open(base_url + '/login')
    #     self.type('#email', 'profile@test.com')
    #     self.type('#password', '123Ab#')
    #     self.click('input[type=\'submit\']')

    #     # update profile
    #     self.open(base_url + '/profile')
    #     self.type('#address', '3 Pancake St')
    #     self.click('input[type=\'submit\']')

    #     # check that it worked
    #     self.assert_element('#address')
    #     self.assert_text('3 Pancake St', '#address')

    # def test_profile_p3(self, *_): 
    #     '''
    #     Partition 3
    #     Update postal code
    #     '''

    #     # login
    #     self.open(base_url + '/login')
    #     self.type('#email', 'profile@test.com')
    #     self.type('#password', '123Ab#')
    #     self.click('input[type=\'submit\']')

    #     # update profile
    #     self.open(base_url + '/profile')
    #     self.type('#postal', 'E6E6E6')
    #     self.click('input[type=\'submit\']')

    #     # check that it worked
    #     self.assert_element('#postal')
    #     self.assert_text('E6E6E6', '#postal')

    # def test_profile_p4(self, *_): 
    #     '''
    #     Partition 4
    #     Update username
    #     '''

    #     # login
    #     self.open(base_url + '/login')
    #     self.type('#email', 'profile@test.com')
    #     self.type('#password', '123Ab#')
    #     self.click('input[type=\'submit\']')

    #     # update profile
    #     self.open(base_url + '/profile')
    #     self.type('#username', 'profile')
    #     self.click('input[type=\'submit\']')

    #     # check that it worked
    #     self.assert_element('#welcome-header')
    #     self.assert_text('Welcome profile !', '#welcome-header')