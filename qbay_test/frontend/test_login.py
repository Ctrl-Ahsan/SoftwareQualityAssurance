# from seleniumbase import BaseCase

# from qbay_test.conftest import base_url
# from unittest.mock import patch
# from qbay.models import User


# class FrontEndHomePageTest(BaseCase):
#     '''
#     The following code is an input coverage test for logging-in.

#     Below is the partition & the inputs with that partition,
#     p1, No email & no password
#     p2, Valid email & non-valid password
#     p3, Non-valid email & valid password
#     p4, Valid email & valid password
#     '''

#     def test_login_p1(self, *_):
#         '''
#         Partition 1
#         No email & no password
#         '''

#         # open login page
#         self.open(base_url + '/login')

#         # click enter button
#         self.click('input[type=\'submit\']')

#         self.assert_element('h1')
#         self.assert_text('Login', 'h1')
