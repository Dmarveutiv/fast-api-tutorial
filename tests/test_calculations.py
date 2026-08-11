from app.cal import add, substract

def test_add():
    print('testing add func')
    assert add(4, 2)== 6
    
     
def test_substract():
    assert substract(5, 2) == 3

test_add()
test_substract()