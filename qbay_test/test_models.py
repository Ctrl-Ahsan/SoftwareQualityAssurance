from sqlalchemy.inspection import inspect
from datetime import datetime
from qbay.models import User, register, login, Product
from qbay.models import createProduct, updateUser, updateProduct


def test_r1_1_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''
    assert register('ur0', 'u0@test.ca', '123Ab#') is True
    assert register('ur1', '', '123Ab#') is False
    assert register('ur2', 'u2@test.ca', '') is False


def test_r1_2_user_register():
    assert inspect(User).primary_key[0].name == 'email'


def test_r1_3_user_register():
    assert register('ura', 'u3@gmail.com', '123Ab#') is True
    assert register('urb', 'u.4@queensu.ca', '123Ab#') is True
    assert register('urc', '.u5@queensu.ca', '123Ab#') is False
    assert register('urd', 'u6.@queensu.ca', '123Ab#') is False
    assert register('ure', 'a..a@hotmail.com', '123Ab#') is False


def test_r1_4_user_register():
    assert register('urf', 'u8@queensu.ca', '123Ab#') is True
    assert register('urg', 'u9@queensu.ca', '12Ab#') is False
    assert register('urh', 'u10@queensu.ca', '123bb#') is False
    assert register('uri', ' u11@queensu.ca', '12AA#') is False
    assert register('urj', 'u12@queensu.ca', '12Ab5') is False


def test_r1_5_user_register():
    assert register('User Thirteen', 'u13@queensu.ca', '123Ab#') is True
    assert register('User', 'u14@queensu.ca', '123Ab#') is True
    assert register('User ', 'u15@queensu.ca', '123Ab#') is False
    assert register(' User', 'u16@queensu.ca', '123Ab#') is False


def test_r1_6_user_register():
    assert register('urq', 'u19@queensu.ca', '123Ab#') is True
    assert register('u', 'u20@queensu.ca', '123Ab#') is False
    assert register('abcdefghijklmnopqrstuv', 'u21@qq.ca', '123Ab#') is False


def test_r1_7_user_register():
    register('urt', 'u22@queensu.ca', '123Ab#')
    result = register('urt', 'u22@queensu.ca', '123Ab#')
    assert result is False


def test_r1_8_user_register():
    register('tmp', 'tmp@queensu.ca', '123Ab#')
    user = User.query.filter_by(email='tmp@queensu.ca').first()
    assert user.shipping_address == ''


def test_r1_9_user_register():
    register('tmp2', 'tmp2@queensu.ca', '123Ab#')
    user = User.query.filter_by(email='tmp2@queensu.ca').first()
    assert user.postal_code == ''


def test_r1_10_user_register():
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
    register('urq', 'u19@queensu.ca', '123Ab#')
    assert updateUser( 'urq', '22 university ave') is True
    assert updateUser('urq', 'urq2') is True
    assert updateUser('urq', 'y2k 1j3') is True
    assert updateUser('urq', 'passyword') is False


def test_r3_2_update_user():
    # test for valid shipping address
    register('urq', 'u19@queensu.ca', '123Ab#')
    assert updateUser('urq', '22 university ave') is True
    assert updateUser('urq', '@@ university ave') is False


def test_r3_3_update_user():
    # test for valid postal code
    register('urq', 'u19@queensu.ca', '123Ab#')
    assert updateUser('urq', 'k2r 1w5') is True
    assert updateUser('urq', 'bb3 77h') is False


def test_r3_4_update_user():
    # test for valid username
    register('urq', 'u19@queensu.ca', '123Ab#')
    assert updateUser('urq', 'urq2') is True
    assert updateUser('urq', 'q') is False


def test_r4_1_create_product():
    # test for valid title characters
    # prefix/sufix!=space, must be alphanumerical
    assert createProduct('title 1', 'description must be twenty chars',
                         10, '2021-10-10', 'u0@test.ca') is True

    assert createProduct(' title 2', 'description must be twenty chars',
                         10, '2021-10-10', 'u0@test.ca') is False

    assert createProduct('title 3 ', 'description must be twenty chars',
                         10, '2021-10-10', 'u0@test.ca') is False

    assert createProduct('title $', 'description must be twenty chars',
                         10, '2021-10-10', 'u0@test.ca') is False


def test_r4_2_create_product():
    # test for valid title length
    # no more than 80 characters
    assert createProduct('title 4', 'description must be twenty chars',
                         10, '2021-10-10', 'u0@test.ca') is True

    assert createProduct('8080808080808080808080808080808080'
                         '8080808080808080808080808080808080'
                         '808080808080', 'description must be twenty chars',
                         10, '2021-10-10', 'u0@test.ca') is False


def test_r4_3_create_product():
    # test for valid description length
    # total charcters between 20 and 2000
    assert createProduct('title 5', 'description must be twenty chars',
                         10, '2021-10-10', 'u0@test.ca') is True

    assert createProduct('title 6', 'description',
                         10, '2021-10-10', 'u0@test.ca') is False

    assert createProduct('title 7', """description must be > 2000
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
    assert createProduct('title 8', 'description must be twenty chars',
                         10, '2021-10-10', 'u0@test.ca') is True

    assert createProduct('title 9 be longer than 20', 'description be twenty',
                         10, '2021-10-10', 'u0@test.ca') is False


def test_r4_5_create_product():
    # test for valid price range
    # between 10 and 10000
    assert createProduct('title 10', 'description must be twenty chars',
                         10, '2021-10-10', 'u0@test.ca') is True

    assert createProduct('title 11', 'description must be twenty chars',
                         9, '2021-10-10', 'u0@test.ca') is False

    assert createProduct('title 12', 'description must be twenty chars',
                         10001, '2021-10-10', 'u0@test.ca') is False


def test_r4_6_create_product():
    # test for valid date
    # must be after 2021-01-02 and before 2025-01-02.
    assert createProduct('title 13', 'description must be twenty chars',
                         10, '2021-10-10', 'u0@test.ca') is True

    assert createProduct('title 14', 'description must be twenty chars',
                         10, '2021-01-01', 'u0@test.ca') is False

    assert createProduct('title 15', 'description must be twenty chars',
                         10, '2026-01-01', 'u0@test.ca') is False


def test_r4_7_create_product():
    # test for valid owner email
    # must be none empty and owner must exist
    assert createProduct('title 16', 'description must be twenty chars',
                         10, '2021-10-10', 'u0@test.ca') is True

    assert createProduct('title 17', 'description must be twenty chars',
                         10, '2021-10-10', 'fakeemail@gmail.com') is False

    assert createProduct('title 18', 'description must be twenty chars',
                         10, '2021-10-10', '') is False


def test_r4_8_create_product():
    # test for unique product title
    assert createProduct('title 19', 'description must be twenty chars',
                         10, '2021-10-10', 'u0@test.ca') is True

    assert createProduct('title 19', 'description must be twenty chars',
                         10, '2021-10-10', 'u0@test.ca') is False


def test_r5_1_update_product():
    # test for update
    createProduct('testtitle', 'description must be twenty chars',
                  10, '2021-10-10', 'u0@test.ca')

    assert updateProduct("testtitle", "new title",
                         "new description must be twenty chars",
                         100) is True

    updatedproduct = Product.query.filter_by(title="new title").first()
    assert (updatedproduct.title == "new title") is True
    assert (updatedproduct.description == "new description must be twenty chars") is True
    assert (updatedproduct.price == 100) is True


def test_r5_2_update_product():
    # test for ensuring price increases
    assert updateProduct("title 16", "new title2",
                         "new description must be twenty chars",
                         200) is True
    assert updateProduct("title 16", "new title3",
                         "new description must be twenty chars",
                         50) is False


def test_r5_3_update_product():
    # test for correct modified date
    assert (updatedproduct.last_modified == datetime.today().strftime('%Y-%m-%d')) is True


def test_r5_4_update_product():
    # testing for prequery checks
    assert updateProduct("title 10", " new title4",
                         "new description must be twenty chars",
                         200) is False

    assert updateProduct("title 10", "new title5 ",
                         "new description must be twenty chars",
                         200) is False

    assert updateProduct("title 10", "new title$",
                         "new description must be twenty chars",
                         200) is False

    assert updateProduct("title 10", "new title6", "short desc",
                         200) is False

    assert updateProduct("title 10", "new title7", """description must be
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

    assert updateProduct("title 10", "new title8",
                         "new description must be twenty chars",
                         9) is False

    assert updateProduct("title 10", "new title9",
                         "new description must be twenty chars",
                         10001) is False
