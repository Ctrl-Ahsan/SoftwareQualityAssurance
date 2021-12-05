# from seleniumbase import BaseCase

# from qbay_test.conftest import base_url
# from unittest.mock import patch
# from qbay.models import User
# import time
# import random
# import string
# from random import randint


# class FrontEndHomePageTest(BaseCase):
#     def test_r4_1_1(self, *_):
#         '''
#         Input coverage
#         '''
#     # open register
#         self.open(base_url + '/register')
#         self.type('#name', 'upupeyy')
#         self.type('#email', 'upupeyy@test.com')
#         self.type('#password', '123Ab#')
#         self.type('#password2', '123Ab#')
#         self.click('input[type=\'submit\']')
        
#         # login
#         self.type('#email', 'upupeyy@test.com')
#         self.type('#password', '123Ab#')
#         self.click('input[type=\'submit\']')

#         # partition 1
#         self.open(base_url + '/create')
#         self.type('#title', '  prefix space')
#         self.type('#description', 'stuff' * 6)
#         self.type('#price', '15')
#         self.click('input[type=\'submit\']')

#         self.assert_element('#message')
#         self.assert_text('Product not created.', '#message')

#     def test_r4_1_2(self, *_):
#         # login
#         self.open(base_url + '/login')
#         self.type('#email', 'upupeyy@test.com')
#         self.type('#password', '123Ab#')
#         self.click('input[type=\'submit\']')

#         # partition 2
#         self.open(base_url + '/create')
#         self.type('#title', 'space at end  ')
#         self.type('#description', 'stuffs' * 6)
#         self.type('#price', '40')
#         self.click('input[type=\'submit\']')

#         self.assert_element('#message')
#         self.assert_text('Product not created.', '#message')

#     def test_r4_1_3(self, *_):
#         self.open(base_url + '/login')
#         # login
#         self.type('#email', 'upupeyy@test.com')
#         self.type('#password', '123Ab#')
#         self.click('input[type=\'submit\']')

#         # partition 3
#         self.open(base_url + '/create')
#         self.type('#title', 'not@alpha')
#         self.type('#description', 'stuffs' * 6)
#         self.type('#price', '25')
#         self.click('input[type=\'submit\']')

#         self.assert_element('#message')
#         self.assert_text('Product not created.', '#message')

#     def test_r4_1_4(self, *_):
#         self.open(base_url + '/login')

#         # login
#         self.type('#email', 'upupeyy@test.com')
#         self.type('#password', '123Ab#')
#         self.click('input[type=\'submit\']')
#         # partition 4
#         self.open(base_url + '/create')
#         self.type('#title', 'bicycle2012')
#         self.type('#description', 'things' * 6)
#         self.type('#price', '50')
#         self.click('input[type=\'submit\']')

#         self.assert_element('#bicycle2012')
#         self.assert_text('name: bicycle2012 price: 50.0', '#bicycle2012')

#     def test_r4_2(self, *_):
#         '''
#         output coverage test
#         '''
#         # open register
#         self.open(base_url + '/register')
#         self.type('#name', 'upupeyyy')
#         self.type('#email', 'upupeyyy@test.com')
#         self.type('#password', '123Ab#')
#         self.type('#password2', '123Ab#')
#         self.click('input[type=\'submit\']')
#         time.sleep(2)

#         # login
#         self.type('#email', 'upupeyyy@test.com')
#         self.type('#password', '123Ab#')
#         self.click('input[type=\'submit\']')

#         # partition 1
#         self.open(base_url + '/create')
#         self.type('#title', 'title' * 5)
#         self.type('#description', 'stuff' * 5)
#         self.type('#price', '180')
#         self.click('input[type=\'submit\']')

#         self.assert_element('#message')
#         self.assert_text('Product not created.', '#message')

#         self.open(base_url + '/register')
#         self.type('#name', 'upupedyy')
#         self.type('#email', 'upupedyy@test.com')
#         self.type('#password', '123Ab#')
#         self.type('#password2', '123Ab#')
#         self.click('input[type=\'submit\']')
#         time.sleep(2)

#         # login
#         self.type('#email', 'upupedyy@test.com')
#         self.type('#password', '123Ab#')
#         self.click('input[type=\'submit\']')

#         # partition 2
#         self.open(base_url + '/create')
#         self.type('#title', 'titles')
#         self.type('#description', 'stuff' * 5)
#         self.type('#price', '60')
#         self.click('input[type=\'submit\']')

#         self.assert_element('#titles')
#         self.assert_text('name: titles price: 60.0', '#titles')
        
#     def test_r4_3(self, *_):
#         '''
#         Boundary testing.
#         '''
#         # open register page
#         self.open(base_url + '/register')
#         self.type('#email', 'lego@test.com')
#         self.type('#name', 'leggo')
#         self.type('#password', '123Ab#')
#         self.type('#password2', '123Ab#')
#         self.click('input[type=\'submit\']')

#         # open login
#         self.type('#email', 'lego@test.com')
#         self.type('#password', '123Ab#')
#         self.click('input[type=\'submit\']')

#         # lower boundary
#         self.open(base_url + '/create')
#         self.type('#title', 'testing')
#         self.type('#description', '123456789abcdefghij')
#         self.type('#price', '10')
#         self.click('input[type=\'submit\']')
#         self.assert_element('#message')
#         self.assert_text('Product not created.')

#         # upper boundary
#         self.open(base_url + '/create')
#         self.type('#title', 'testing2')
#         d = ''.join(random.choice(string.ascii_lowercase) for x in range(2002))
#         self.type('#description', d)
#         self.type('#price', '10')
#         self.click('input[type=\'submit\']')
#         self.assert_element('#message')
#         self.assert_text('Product not created.')

#     def test_r4_4(self, *_):
#         # open register page
#         self.open(base_url + '/register')
#         self.type('#email', 'short@test.com')
#         self.type('#name', 'short')
#         self.type('#password', '123Ab#')
#         self.type('#password2', '123Ab#')
#         self.click('input[type=\'submit\']')
        
#         # open login
#         self.type('#email', 'short@test.com')
#         self.type('#password', '123Ab#')
#         self.click('input[type=\'submit\']')
        
#         # partition 1
#         self.open(base_url + '/create')
#         self.type('#title', 'temp')
#         self.type('#description', 'tempatempatempatempatempa')
#         self.type('#price', '10')
#         self.click('input[type=\'submit\']')
#         self.assert_element('#temp')
#         self.assert_text('name: temp price: 10.0')

#         # partition 2
#         self.open(base_url + '/create')
#         self.type('#title', 'temptemptemptemptemptemptemptemp')
#         self.type('#description', 'tempatempatempatempatempa')
#         self.type('#price', '10')
#         self.click('input[type=\'submit\']')
#         self.assert_element('#message')
#         self.assert_text('Product not created.')
        
#     def test_r4_5(self, *_):
#         '''
#         Shotgun testing
#         Randomly input different prices
#         '''
#         # open register
#         self.open(base_url + '/register')
#         self.type('#name', 'upupey')
#         self.type('#email', 'upupey@test.com')
#         self.type('#password', '123Ab#')
#         self.type('#password2', '123Ab#')
#         self.click('input[type=\'submit\']')
#         time.sleep(2)

#         # login
#         self.type('#email', 'upupey@test.com')
#         self.type('#password', '123Ab#')
#         self.click('input[type=\'submit\']')

#         # shotgun
#         for i in range(1, 10):
#             price = randint(10, 10000)
#             self.open(base_url + '/create')
#             self.type('#title', 'up' * i)
#             self.type('#description', 'upupp' * 6)
#             self.type('#price', str(price))
#             self.click('input[type=\'submit\']')
#             self.open(base_url + '/create')

#         # test that it didn't fail
#         self.open(base_url)
#         self.assert_element('h2')
#         self.assert_text('Welcome upupey !', 'h2')
        
#     def test_r4_6(self, *_):
#         '''
#         output coverage test
#         '''
#         # open register
#         self.open(base_url + '/register')
#         self.type('#name', 'upupeyyyy')
#         self.type('#email', 'upupeyyyy@test.com')
#         self.type('#password', '123Ab#')
#         self.type('#password2', '123Ab#')
#         self.click('input[type=\'submit\']')

#         # login
#         self.type('#email', 'upupeyyyy@test.com')
#         self.type('#password', '123Ab#')
#         self.click('input[type=\'submit\']')

#         # output coverage
#         self.open(base_url + '/create')
#         self.type('#title', 'upy')
#         self.type('#description', 'stuff' * 5)
#         self.type('#price', '50')
#         self.click('input[type=\'submit\']')
#         # Update Product
#         self.open(base_url + '/update/upy')
#         self.type('#price', '102')
#         self.click('input[type=\'submit\']')
#         self.open(base_url + '/update/upy')

#         # check for modified date
#         self.assert_element('#modified')
    
#     def test_r4_7(self, *_):
#         '''
#         Input coverage
#         '''
#         # open register page
#         self.open(base_url + '/register')
#         self.type('#email', 'raptor@test.com')
#         self.type('#name', 'raptor')
#         self.type('#password', '123Ab#')
#         self.type('#password2', '123Ab#')
#         self.click('input[type=\'submit\']')
        
#         # case 1 - user tries to create product without being logged in
#         self.open(base_url + '/create')
#         self.assert_element('h1')
#         self.assert_text('Login', 'h1')

#         # login
#         self.type('#email', 'raptor@test.com')
#         self.type('#password', '123Ab#')
#         self.click('input[type=\'submit\']')

#         # case 2 - user tries to create product while logged in
#         self.open(base_url + '/create')
#         self.type('#title', 'something')
#         self.type('#description', 'super something is something')
#         self.type('#price', 10)
#         self.click('input[type=\'submit\']')

#         # test that it didn't fail
#         self.open(base_url)
#         self.assert_element('#something')
#         self.assert_text('name: something price: 10.0')
    
#     def test_r4_8(self, *_):
#         # open register page
#         self.open(base_url + '/register')
#         self.type('#email', 'sametitle@test.com')
#         self.type('#name', 'same')
#         self.type('#password', '123Ab#')
#         self.type('#password2', '123Ab#')
#         self.click('input[type=\'submit\']')
        
#         # login
#         self.type('#email', 'sametitle@test.com')
#         self.type('#password', '123Ab#')
#         self.click('input[type=\'submit\']')

#         # partition 1
#         self.open(base_url + '/create')
#         self.type('#title', 'abcb')
#         self.type('#description', 'abcbbabcbbabcbbabcbbabcbbabcbb')
#         self.type('#price', 10)
#         self.click('input[type=\'submit\']')

#         self.assert_element('#abcb')
#         self.assert_text('name: abcb price: 10.0')

#         # partition 2
#         self.open(base_url + '/create')
#         self.type('#title', 'abcb')
#         self.type('#description', 'abcbbabcbbabcbbabcbbabcbbabcbb')
#         self.type('#price', 10)
#         self.click('input[type=\'submit\']')

#         self.assert_element('#message')
#         self.assert_text('Product not created', '#message')
