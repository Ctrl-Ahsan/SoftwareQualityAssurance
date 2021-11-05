from seleniumbase import BaseCase

from qbay_test.conftest import base_url
import time


class FrontEndHomePageTest(BaseCase):
        
    def test_r5_1(self, *_):
        '''
        Output coverage

        Partition 1
        Update title, description, & price
        Output new information

        Partition 2
        Failed update
        Output should be that the product was not updated
        '''

        # open register page
        self.open(base_url + '/register')
        self.type('#email', 'update@test.com')
        self.type('#name', 'update')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        self.click('input[type=\'submit\']')

        # login
        self.type('#email', 'update@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # create product
        self.open(base_url + '/create')
        self.type('#title', 'updateAbc')
        self.type('#description', 'abcde' * 5)
        self.type('#price', '10')
        self.click('input[type=\'submit\']')

        # partition 1
        self.open(base_url + '/update/updateAbc')
        self.type('#title', 'uABC')
        self.type('#description', 'uABC' * 10)
        self.type('#price', '102')
        self.click('input[type=\'submit\']')

        self.assert_element('#uABC')
        self.assert_text('name: uABC price: 102.0', '#uABC')

        # partition 2
        self.open(base_url + '/update/uABC')
        self.type('#title', '123')
        self.type('#description', 'uABC')
        self.type('#price', '10')
        self.click('input[type=\'submit\']')
        self.assert_element('#message')
        self.assert_text('Product not updated.', '#message')

    def test_r5_2(self, *_):
        '''
        Input coverage

        Partition 1
        Lower price
        Should not fail

        Partition 2
        Same price
        Should not fail

        Partition 3
        Higher price
        Should not fail
        '''
        
        # open register page
        self.open(base_url + '/register')
        self.type('#email', 'updater5@test.com')
        self.type('#name', 'updater5')
        self.type('#password', '123Ab#')
        self.type('#password2', '123Ab#')
        self.click('input[type=\'submit\']')

        # login
        self.type('#email', 'updater5@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        # create product
        self.open(base_url + '/create')
        self.type('#title', 'rFiveTwo')
        self.type('#description', 'rFiveTwo' * 5)
        self.type('#price', '11')
        self.click('input[type=\'submit\']')

        # partition 1
        self.open(base_url + '/update/rFiveTwo')
        self.type('#price', '10')
        self.click('input[type=\'submit\']')
        
        self.assert_element('h1')
        self.assert_text('Update Product', 'h1')

        # partition 2
        self.open(base_url + '/update/rFiveTwo')
        self.type('#price', '11')
        self.click('input[type=\'submit\']')

        self.assert_element('h3')
        self.assert_text('Information', 'h3')

        # partition 3
        self.open(base_url + '/update/rFiveTwo')
        self.type('#price', '12')
        self.click('input[type=\'submit\']')

        self.assert_element('h3')
        self.assert_text('Information', 'h3')




