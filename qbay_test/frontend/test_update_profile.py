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
