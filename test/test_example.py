import pytest
def test_equal_or_not_equal():
    assert 3==3
    # assert 3==2
    # assert 3!=3
    assert 3!=2


def test_is_instance():
    assert isinstance('this is a string',str)
    assert not isinstance('10',int)

def test_boolean():
    val=True
    assert val is True
    assert ('hello'=='world') is False

def test_type():
    assert type('hello' is str)
    assert type('World' is not int)


class Student:
    def __init__(self,first_name:str,last_name:str,major:str,years:int):
        self.first_name=first_name
        self.last_name=last_name
        self.major=major
        self.years=years


@pytest.fixture
def default_emloyee():
    return Student('John','Doe','Computer Science',3)

def test_person_initialization(default_emloyee):
    # p=Student('Joh n','Doe','Computer Science',3)
    assert default_emloyee.first_name=='John' ,'First name should be John'
    assert default_emloyee.last_name=='Doe','Last name should be Doe'
    assert default_emloyee.major=='Computer Science'
    assert default_emloyee.years==3