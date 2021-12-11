from seleniumbase import BaseCase
from selenium import *

from qbay_test.conftest import base_url
from unittest.mock import create_autospec, patch
from qbay.models import User, create_product, register, update_user
from datetime import datetime
import time
import random
import string
from random import randint


class FrontEndHomePageTest(BaseCase):
    def test_1(self, *_):
        # Test that you can buy a product
        self.open(base_url)
        register(
            'frontendBuyer', 
            'frontendBuyer@test.com',
            '123Ab#'
        )
        register(
            'frontendSeller', 
            'frontendSeller@test.com',
            '123Ab#'
        )

        update_user(
            'frontendBuyer', 
            'frontendBuyer', 
            '2 Pancake',
            'L1E2E6'
        )

        print(create_product(
            'frontendProduct',
            'front' * 50,
            10,
            datetime.today().strftime('%Y-%m-%d'),
            'frontendSeller@test.com'
        ))

        create_product(
            'frontendPricey',
            'front' * 50,
            1000,
            datetime.today().strftime('%Y-%m-%d'),
            'frontendSeller@test.com'
        )

        self.type('#email', 'frontendBuyer@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')
        
        self.click('a[id=\'frontendProductBuy\']')

        self.assert_element('#balance')
        self.assert_text('90.0', '#balance')

    def test_2(self, *_):
        # Test that you cannot buy a pricey item
        self.open(base_url)
        self.type('#email', 'frontendBuyer@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        self.click('a[id=\'frontendPriceyBuy\']')

        self.assert_element('#frontendPricey')
        self.assert_text('name: frontendPricey price: 1000.0 buy', '#frontendPricey')

    def test_3(self, *_):
        # Test that a bought item appears on the new owner's page
        self.open(base_url)
        self.type('#email', 'frontendBuyer@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')

        current_date = datetime.today().strftime('%Y-%m-%d')
        self.assert_element('#frontendProduct')
        self.assert_text(
            'name: frontendProduct price: 10.0 purchase date: ' + current_date,
            '#frontendProduct'
        )

    def test_4(self, *_):
        # Test that a bought item no longer appears on the seller's page
        self.open(base_url)
        self.type('#email', 'frontendSeller@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')
        self.assert_element_not_present('#frontendProduct')

    def test_5(self, *_):
        # Test that a user cannot buy their own product.
        self.open(base_url)
        self.type('#email', 'frontendSeller@test.com')
        self.type('#password', '123Ab#')
        self.click('input[type=\'submit\']')
        self.assert_element('#frontendPricey')
        self.assert_text('name: frontendPricey price: 1000.0 update', '#frontendPricey')
