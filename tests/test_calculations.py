import pytest
from app.cal import add, substract, BankAccount

@pytest.fixture
def get_bank_user():
    return BankAccount(50, 'dan')


@pytest.mark.parametrize("num1, num2, expected" , argvalues=[
    (4, 2, 6),
    (3, 4, 7),
    (2, 3, 5),
])
def test_add(num1, num2, expected):
    print('testing add func')
    assert add(num1, num2)== expected
    
@pytest.mark.parametrize("num1, num2, expected", argvalues=[
   (5, 3, 2),
   (9, 6, 3) 
])    
def test_substract(num1, num2, expected):
    assert substract(num1, num2) == expected

def test_bank_balance_user(get_bank_user):
    assert get_bank_user.balance == 50 and get_bank_user.user == 'dan'
    
def test_deposit(get_bank_user):
    get_bank_user.deposit(40)
    assert get_bank_user.balance == 90 
    
def test_withdraw(get_bank_user):
    get_bank_user.withdraw(30)
    assert get_bank_user.balance == 20
 


def test_history(get_bank_user):
    get_bank_user.deposit(40)
    get_bank_user.withdraw(20)
    get_bank_user.deposit(20)
    assert get_bank_user.history == [90,70,90]
    
    
@pytest.mark.parametrize("n1, n2, expected", argvalues=[
    (40, 20, [90, 70]),
    (20, 20, [70, 50]),
    (40, 70, [90, 20])
])
def test_trans(get_bank_user, n1, n2,expected):
    get_bank_user.deposit(n1)
    get_bank_user.withdraw(n2)
    assert get_bank_user.history == expected
    
    
    
# test_withdraw()
# test_deposit()   
# test_bank_balance_user()
# test_history()
