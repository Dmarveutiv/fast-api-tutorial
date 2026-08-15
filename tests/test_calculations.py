import pytest
from app.cal import add, substract


@pytest.mark.parametrize("num1, num2, expected" , argvalues=[
    (4, 2, 6),
    (3, 4, 7),
    (2, 3, 5),
])
def test_add(num1, num2, expected):
    print('testing add func')
    assert add(num1, num2)== expected
    
     
def test_substract():
    assert substract(5, 2) == 3

test_substract()