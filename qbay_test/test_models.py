from qbay.models import User, register, login
from sqlalchemy.inspection import inspect


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


def test_r4_1_create_product():
    # test for valid title characters
    # prefix/sufix!=space, must be alphanumerical
    assert createProduct('title 1', 'description must be twenty chars', 
                         10, '2021-10-10', 'email1@gmail.com') is True

    assert createProduct(' title 2', 'description must be twenty chars', 
                         10, '2021-10-10', 'email1@gmail.com') is False

    assert createProduct('title 3 ', 'description must be twenty chars', 
                         10, '2021-10-10', 'email1@gmail.com') is False      

    assert createProduct('title $', 'description must be twenty chars', 
                         10, '2021-10-10', 'email1@gmail.com') is False


def test_r4_2_create_product():
    # test for valid title length
    # no more than 80 characters
    assert createProduct('title 4', 'description must be twenty chars', 
                         10, '2021-10-10', 'email1@gmail.com') is True

    assert createProduct('8080808080808080808080808080808080'
                         '8080808080808080808080808080808080'
                         '808080808080', 'description must be twenty chars', 
                         10, '2021-10-10', 'email1@gmail.com') is False    


def test_r4_3_create_product():
    # test for valid description length
    # total charcters between 20 and 2000
    assert createProduct('title 5', 'description must be twenty chars', 
                         10, '2021-10-10', 'email1@gmail.com') is True  

    assert createProduct('title 6', 'description', 
                         10, '2021-10-10', 'email1@gmail.com') is False

    assert createProduct('title 7', 'description must be > 2000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000'
                         '200020002000200020002000200020002000200020002000', 
                         10, '2021-10-10', 'email1@gmail.com') is False        


def test_r4_4_create_product():
    # test that description is longer than title
    assert createProduct('title 8', 'description must be twenty chars', 
                         10, '2021-10-10', 'email1@gmail.com') is True 

    assert createProduct('title 9 be longer than 20', 'description be twenty', 
                         10, '2021-10-10', 'email1@gmail.com') is False                           


def test_r4_5_create_product():
    # test for valid price range
    # between 10 and 10000
    assert createProduct('title 10', 'description must be twenty chars', 
                         10, '2021-10-10', 'email1@gmail.com') is True  

    assert createProduct('title 11', 'description must be twenty chars', 
                         9, '2021-10-10', 'email1@gmail.com') is False

    assert createProduct('title 12', 'description must be twenty chars', 
                         10001, '2021-10-10', 'email1@gmail.com') is False


def test_r4_6_create_product():
    # test for valid date
    # must be after 2021-01-02 and before 2025-01-02.
    assert createProduct('title 13', 'description must be twenty chars', 
                         10, '2021-10-10', 'email1@gmail.com') is True   

    assert createProduct('title 14', 'description must be twenty chars', 
                         10, '2021-01-01', 'email1@gmail.com') is False

    assert createProduct('title 15', 'description must be twenty chars', 
                         10, '2026-01-01', 'email1@gmail.com') is False      


def test_r4_7_create_product():
    # test for valid owner email
    # must be none empty and owner must exist
    assert createProduct('title 16', 'description must be twenty chars', 
                         10, '2021-10-10', 'email1@gmail.com') is True  

    assert createProduct('title 17', 'description must be twenty chars', 
                         10, '2021-10-10', 'fakeemail@gmail.com') is False    

    assert createProduct('title 18', 'description must be twenty chars', 
                         10, '2021-10-10', '') is False    


def test_r4_8_create_product():
    # test for unique product title
    assert createProduct('title 19', 'description must be twenty chars', 
                         10, '2021-10-10', 'email1@gmail.com') is True 

    assert createProduct('title 19', 'description must be twenty chars', 
                         10, '2021-10-10', 'email1@gmail.com') is False 