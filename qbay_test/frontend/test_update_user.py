from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from qbay.models import bypass_register


class FrontEndHomePageTest(BaseCase):
    def test_r3_1(self, *_):
        '''
        Output coverage.
        '''
        # register
        bypass_register('r3_1', 'r3_1@test.com', 'Test123$')

        # login
        self.open(base_url + '/login')
        self.type('#email', 'r3_1@test.com')
        self.type('#password', 'Test123$')
        self.click('input[type=\'submit\']')

        # update profile failed
        self.open(base_url + '/profile')
        self.type('#address', 'queens')
        self.click('input[type=\'submit\']')
        self.assert_element('#message')
        self.assert_text('Profile not updated.', '#message')

        # update profile succeeded
        self.type('#username', 'alligator7')
        self.type('#address', 'queens')
        self.type('#postal', 'A1B2C3')
        self.click('input[type=\'submit\']')
        self.assert_element('h2')
        self.assert_text('Welcome alligator7 !', 'h2')
        self.assert_element('#address')
        self.assert_text('queens', '#address')
        self.assert_element('#postal')
        self.assert_text('A1B2C3', '#postal')

    def test_r3_2(self, *_):
        '''
        Input Partition
        '''
        # register
        bypass_register('r3_2', 'r3_2@test.com', 'Test123$')

        # login
        self.open(base_url + '/login')
        self.type('#email', 'r3_2@test.com')
        self.type('#password', 'Test123$')
        self.click('input[type=\'submit\']')

        # partition 1 - empty address
        self.open(base_url + '/profile')
        self.type('#address', '')
        self.type('#postal', 'A1B2C3')
        self.click('input[type=\'submit\']')
        self.assert_element('#message')
        self.assert_text('Profile not updated.', '#message')

        # partition 2 - address with special characters
        self.type('#address', 'queen$')
        self.type('#postal', 'A1B2C3')
        self.click('input[type=\'submit\']')
        self.assert_element('#message')
        self.assert_text('Profile not updated.', '#message')

        # partition 3 - valid address
        self.type('#address', 'queens')
        self.type('#postal', 'A1B2C3')
        self.click('input[type=\'submit\']')
        self.assert_element('#address')
        self.assert_text('queens', '#address')
        self.assert_element('#postal')
        self.assert_text('A1B2C3', '#postal')

    def test_r3_3(self, *_):
        '''
        Output coverage
        '''
        # register
        bypass_register('r3_3', 'r3_3@test.com', 'Test123$')

        # login
        self.open(base_url + '/login')
        self.type('#email', 'r3_3@test.com')
        self.type('#password', 'Test123$')
        self.click('input[type=\'submit\']')

        # invalid postal code
        self.open(base_url + '/profile')
        self.type('#address', 'queens')
        self.type('#postal', '11111')
        self.click('input[type=\'submit\']')
        self.assert_element('#message')
        self.assert_text('Profile not updated.', '#message')

        # valid postal code
        self.type('#address', 'queens')
        self.type('#postal', 'A1B2C3')
        self.click('input[type=\'submit\']')
        self.assert_element('#postal')
        self.assert_text('A1B2C3', '#postal')

    def test_r3_4(self, *_):
        '''
        Input partition
        '''
        # register
        bypass_register('r3_4', 'r3_4@test.com', 'Test123$')

        # login
        self.open(base_url + '/login')
        self.type('#email', 'r3_4@test.com')
        self.type('#password', 'Test123$')
        self.click('input[type=\'submit\']')

        # partition 1 - empty username
        self.open(base_url + '/profile')
        self.clear('#username')
        self.type('#address', 'queens')
        self.type('#postal', 'A1B2C3')
        self.click('input[type=\'submit\']')
        self.assert_element('#message')
        self.assert_text('Profile not updated.', '#message')

        # partition 2 - short username
        self.type('#username', 'a')
        self.type('#address', 'queens')
        self.type('#postal', 'A1B2C3')
        self.click('input[type=\'submit\']')
        self.assert_element('#message')
        self.assert_text('Profile not updated.', '#message')

        # partition 3 - long username
        self.type('#username', 'a123456789a123456789')
        self.type('#address', 'queens')
        self.type('#postal', 'A1B2C3')
        self.click('input[type=\'submit\']')
        self.assert_element('#message')
        self.assert_text('Profile not updated.', '#message')

        # partition 4 - space in prefix/suffix
        self.type('#username', ' legoelego')
        self.type('#address', 'queens')
        self.type('#postal', 'A1B2C3')
        self.click('input[type=\'submit\']')
        self.assert_element('#message')
        self.assert_text('Profile not updated.', '#message')
        self.type('#username', 'legoelego ')
        self.type('#address', 'queens')
        self.type('#postal', 'A1B2C3')
        self.click('input[type=\'submit\']')
        self.assert_element('#message')
        self.assert_text('Profile not updated.', '#message')

        # partition 5 - valid username
        self.type('#username', 'sorandommmm')
        self.type('#address', 'queens')
        self.type('#postal', 'A1B2C3')
        self.click('input[type=\'submit\']')
        self.assert_element('h2')
        self.assert_text('Welcome sorandommmm !', 'h2')