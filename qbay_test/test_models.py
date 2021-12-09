from sqlalchemy.inspection import inspect
from datetime import datetime
from qbay.models import User, buy_product, register, login, Product
from qbay.models import create_product, update_user, update_product
from qbay.models import buy_product


def test_r1_1_user_register():
    # Test that both the email and password cannot be empty
    assert register('ur0', 'u0@test.ca', '123Ab#') is True
    assert register('ur1', '', '123Ab#') is False
    assert register('ur2', 'u2@test.ca', '') is False


def test_r1_2_user_register():
    # Test that user is uniquely identified by his/her email address
    register('abcdefg', 'abc@abc.ca', '123Ab#')
    register('abcde', 'abc@abc.ca', '123Ab#')
    users = list(User.query.filter_by(email='abc@abc.ca'))
    assert len(users) == 1


def test_r1_3_user_register():
    # Test that email follows RFC 5322
    assert register('ura', 'u3@gmail.com', '123Ab#') is True
    assert register('urb', 'u.4@queensu.ca', '123Ab#') is True
    assert register('urc', '.u5@queensu.ca', '123Ab#') is False
    assert register('urd', 'u6.@queensu.ca', '123Ab#') is False
    assert register('ure', 'a..a@hotmail.com', '123Ab#') is False


def test_r1_4_user_register():
    # Test that password has,
    # 1. at least a length of 6
    # 2. at least 1 upper case
    # 3. has 1 or more lower cases
    # 4. and at least 1 special case

    assert register('urf', 'u8@queensu.ca', '123Ab#') is True
    assert register('urg', 'u9@queensu.ca', '12Ab#') is False
    assert register('urh', 'u10@queensu.ca', '123bb#') is False
    assert register('uri', ' u11@queensu.ca', '12AA#') is False
    assert register('urj', 'u12@queensu.ca', '12Ab5') is False


def test_r1_5_user_register():
    # Tests that username is alphanumeric-only and can allow spaces
    assert register('User Thirteen', 'u13@queensu.ca', '123Ab#') is True
    assert register('User', 'u14@queensu.ca', '123Ab#') is True
    assert register('User ', 'u15@queensu.ca', '123Ab#') is False
    assert register(' User', 'u16@queensu.ca', '123Ab#') is False


def test_r1_6_user_register():
    # Tests that username must be > 2 or < 20 characters
    assert register('urq', 'u19@queensu.ca', '123Ab#') is True
    assert register('u', 'u20@queensu.ca', '123Ab#') is False
    assert register('abcdefghijklmnopqrstuv', 'u21@qq.ca', '123Ab#') is False


def test_r1_7_user_register():
    # Tests that you cannot register with a used email
    register('urt', 'u22@queensu.ca', '123Ab#')
    result = register('urt', 'u22@queensu.ca', '123Ab#')
    assert result is False


def test_r1_8_user_register():
    # Tests that shipping address is empty
    register('tmp', 'tmp@queensu.ca', '123Ab#')
    user = User.query.filter_by(email='tmp@queensu.ca').first()
    assert user.shipping_address == ''


def test_r1_9_user_register():
    # Tests that postal code is empty
    register('tmp2', 'tmp2@queensu.ca', '123Ab#')
    user = User.query.filter_by(email='tmp2@queensu.ca').first()
    assert user.postal_code == ''


def test_r1_10_user_register():
    # Tests that balance is 100
    register('tmp3', 'tmp3@queensu.ca', '123Ab#')
    user = User.query.filter_by(email='tmp3@queensu.ca').first()
    assert user.balance == 100.0


def test_r2_1_login():
    # test login functionality
    testuser = login("u3@gmail.com", "123Ab#")
    assert testuser is not None

    testuser2 = login("u3@gmail.com", "wrongpassword")
    assert testuser2 is None

    testuser3 = login("notregistered@gmail.com", "123Ab#")
    assert testuser3 is None


def test_r2_2_login():
    # test for pre query checks
    testuser4 = login("u3@gmail.com", "123Ab#")
    assert testuser4 is not None

    testuser5 = login("", "123Ab#")
    assert testuser5 is None

    testuser6 = login("u3@gmail.com", "")
    assert testuser6 is None


def test_r3_1_update_user():
    # test for exclusice user update fields
    register('tempuser', 'temp19@queensu.ca', '123Ab#')

    assert update_user('tempuser', 'newtempuser',
                       '22 university ave', 'y2k 1j3') is True

    updatedUser = User.query.filter_by(username="newtempuser").first()
    assert (updatedUser.username == 'newtempuser') is True
    assert (updatedUser.shipping_address == '22 university ave') is True
    assert (updatedUser.postal_code == 'y2k 1j3') is True


def test_r3_2_update_user():
    # test for valid shipping address
    register('urqf', 'u299@queensu.ca', '123Ab#')
    assert update_user('urqf', 'urqf', '22 university ave', 'y2k 1j3') is True
    assert update_user('urqf', 'urqf', '@@ university ave', 'y2k 1j3') is False


def test_r3_3_update_user():
    # test for valid postal code
    register('urq223', '233q@queensu.ca', '123Ab#')
    assert update_user('urq223', 'urq223', '22 universty', 'k2r 1w5') is True
    assert update_user('urq223', 'urq223', '22 universty', 'z2r rw5') is False


def test_r3_4_update_user():
    # test for valid username
    register('urq9', 'u133@queensu.ca', '123Ab#')
    assert update_user('urq9', 'urq9', '22 universty', 'k2r 1w5') is True
    assert update_user('urq9', 'u', '22 universty', 'k2r 1w5') is False
    assert update_user('urq9', '', '22 universty', 'k2r 1w5') is False
    assert update_user('urq9', 'A$AP ROCK', '22 universty', 'k2r 1w5') is False
    assert update_user('urq9', ' qrr', '22 universty', 'k2r 1w5') is False
    assert update_user('urq9', 'qrr ', '22 universty', 'k2r 1w5') is False
    assert update_user('urq9', 'wwwwwwwwwwwwwwwwwwwwwwwww',
                       '22 universty', 'k2r 1w5') is False


def test_r4_1_create_product():
    # test for valid title characters
    # prefix/sufix!=space, must be alphanumerical
    assert create_product('title 1', 'description must be twenty chars',
                          10, '2021-10-10', 'u0@test.ca') is True

    assert create_product(' title 2', 'description must be twenty chars',
                          10, '2021-10-10', 'u0@test.ca') is False

    assert create_product('title 3 ', 'description must be twenty chars',
                          10, '2021-10-10', 'u0@test.ca') is False

    assert create_product('title $', 'description must be twenty chars',
                          10, '2021-10-10', 'u0@test.ca') is False


def test_r4_2_create_product():
    # test for valid title length
    # no more than 80 characters
    assert create_product('title 4', 'description must be twenty chars',
                          10, '2021-10-10', 'u0@test.ca') is True

    assert create_product('8080808080808080808080808080808080'
                          '8080808080808080808080808080808080'
                          '808080808080', 'description must be twenty chars',
                          10, '2021-10-10', 'u0@test.ca') is False


def test_r4_3_create_product():
    # test for valid description length
    # total charcters between 20 and 2000
    assert create_product('title 5', 'description must be twenty chars',
                          10, '2021-10-10', 'u0@test.ca') is True

    assert create_product('title 6', 'description',
                          10, '2021-10-10', 'u0@test.ca') is False

    assert create_product('title 7', """description must be > 2000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000""",
                          10, '2021-10-10', 'u0@test.ca') is False


def test_r4_4_create_product():
    # test that description is longer than title
    assert create_product('title 8', 'description must be twenty chars',
                          10, '2021-10-10', 'u0@test.ca') is True

    assert create_product('title 9 be longer than 20', 'description be twenty',
                          10, '2021-10-10', 'u0@test.ca') is False


def test_r4_5_create_product():
    # test for valid price range
    # between 10 and 10000
    assert create_product('title 10', 'description must be twenty chars',
                          10, '2021-10-10', 'u0@test.ca') is True

    assert create_product('title 11', 'description must be twenty chars',
                          9, '2021-10-10', 'u0@test.ca') is False

    assert create_product('title 12', 'description must be twenty chars',
                          10001, '2021-10-10', 'u0@test.ca') is False


def test_r4_6_create_product():
    # test for valid date
    # must be after 2021-01-02 and before 2025-01-02.
    assert create_product('title 13', 'description must be twenty chars',
                          10, '2021-10-10', 'u0@test.ca') is True

    assert create_product('title 14', 'description must be twenty chars',
                          10, '2021-01-01', 'u0@test.ca') is False

    assert create_product('title 15', 'description must be twenty chars',
                          10, '2026-01-01', 'u0@test.ca') is False


def test_r4_7_create_product():
    # test for valid owner email
    # must be none empty and owner must exist
    assert create_product('title 16', 'description must be twenty chars',
                          10, '2021-10-10', 'u0@test.ca') is True

    assert create_product('title 17', 'description must be twenty chars',
                          10, '2021-10-10', 'fakeemail@gmail.com') is False

    assert create_product('title 18', 'description must be twenty chars',
                          10, '2021-10-10', '') is False


def test_r4_8_create_product():
    # test for unique product title
    assert create_product('title 19', 'description must be twenty chars',
                          10, '2021-10-10', 'u0@test.ca') is True

    assert create_product('title 19', 'description must be twenty chars',
                          10, '2021-10-10', 'u0@test.ca') is False


def test_r5_1_update_product():
    # test for update
    create_product('testtitle', 'description must be twenty chars',
                   10, '2021-10-10', 'u0@test.ca')

    assert update_product("testtitle", "new title",
                          "new description must be twenty chars",
                          100) is True

    updatedproduct = Product.query.filter_by(title="new title").first()
    testString = "new description must be twenty chars"
    assert (updatedproduct.title == "new title") is True
    assert (updatedproduct.description == testString) is True
    assert (updatedproduct.price == 100) is True


def test_r5_2_update_product():
    # test for ensuring price increases
    assert update_product("title 16", "new title2",
                          "new description must be twenty chars",
                          200) is True
    assert update_product("title 16", "new title3",
                          "new description must be twenty chars",
                          50) is False


def test_r5_3_update_product():
    # test for correct modified date
    updatedproduct = Product.query.filter_by(title="new title").first()
    today = datetime.today().strftime('%Y-%m-%d')
    assert (updatedproduct.last_modified == today) is True


def test_r5_4_update_product():
    # testing for prequery checks
    assert update_product("title 10", " new title4",
                          "new description must be twenty chars",
                          200) is False

    assert update_product("title 10", "new title5 ",
                          "new description must be twenty chars",
                          200) is False

    assert update_product("title 10", "new title$",
                          "new description must be twenty chars",
                          200) is False

    assert update_product("title 10", "new title6", "short desc",
                          200) is False

    assert update_product("title 10", "new title7", """description must be
                          > 2000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000
                          200020002000200020002000200020002000200020002000""",
                          200) is False

    assert update_product("title 10", "new title8",
                          "new description must be twenty chars",
                          9) is False

    assert update_product("title 10", "new title9",
                          "new description must be twenty chars",
                          10001) is False


def test_r6_1_place_order():
    # testing if a user can order a product
    user = User.query.filter_by(email='u299@queensu.ca').first()
    assert buy_product('title 1', user) is True
    assert buy_product('nottestsale', 'u299@queensu.ca') is False


def test_r6_2_place_order():
    # testing if a user can order their own product
    user = User.query.filter_by(email='u0@test.ca').first()
    assert buy_product('title 8', user) is False


def test_r6_3_place_order():
    # testing if a user can order a product valued more than their balance
    user = User.query.filter_by(email='u299@queensu.ca').first()
    assert buy_product('title 4', user) is True
    assert buy_product('new title2', user) is False
