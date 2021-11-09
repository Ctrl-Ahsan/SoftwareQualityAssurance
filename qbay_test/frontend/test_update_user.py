from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from qbay.models import bypass_register


class FrontEndHomePageTest(BaseCase):
    def test_r3_1(self, *_):
        '''
        Output coverage.
        '''
        # register
        bypass_register("Tester", "tester@test.com", "Test123$")

        # login
        self.open(base_url + '/login')
        self.type('#email', 'tester@test.com')
        self.type('#password', 'Test123$')
        self.click('input[type=\'submit\']')

        # update profile
        self.open(base_url + '/profile')
        self.type('#username', 'Testing')
        self.type('#address', 'queens')
        self.type('#postal', 'A1B2C3')
        self.click('input[type=\'submit\']')

        # test if updated information is displayed properly
        self.assert_element('#address')
        self.assert_text('queens', '#address')
        self.assert_element('#postal')
        self.assert_text('A1B2C3', '#postal')