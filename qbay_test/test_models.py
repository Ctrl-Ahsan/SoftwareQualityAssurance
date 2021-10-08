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
    assert register('abcdefghijklmnopqrstuvwxyz', 'u21@queensu.ca', '123Ab#') is False

# def test_r1_7_user_register():
#     assert register('urt', 'u22@queensu.ca', '123Ab#') is True
#     assert register('urt', 'u22@queenu.ca', '123Ab#') is False

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
