# test_specs.py
"""Volume 1B: Testing.
Bailey Smith
Math 347
January 4 2017
"""

import math
import specs
import pytest

# Tests the addition and fibonacci functions from specs.py
def test_addition():
    assert specs.addition(2,2) == 4, "Addition failed on positive integers"
    assert specs.addition(-1,-8) == -9, "Addition failed on negative integers"
    assert specs.addition(1,-1) == 0

def test_smallest_factor():
    assert specs.smallest_factor(1) == 1, "Smallest_factor failed for 1"
    assert specs.smallest_factor(5) == 5, "Smallest_factor failed for prime number"
    assert specs.smallest_factor(6) == 2, "Smallest_factor failed for composite number"

# Tests the operator function from specs.py
def test_operator():
    with pytest.raises(Exception) as excinfo:
        specs.operator(4,0,1)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Oper should be a string"

    with pytest.raises(Exception) as excinfo:
        specs.operator(4,0,'+=')
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Oper should be one character"

    with pytest.raises(Exception) as excinfo:
        specs.operator(4,0,'/')
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "You can't divide by zero!"

    with pytest.raises(Exception) as excinfo:
        specs.operator(4,0,'1')
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Oper can only be: '+', '/', '-', or '*'"

    assert specs.operator(4,1,'+') == 5, "Opertator failed for addition"
    assert specs.operator(4,1,'/') == 4, "Opertator failed for division"
    assert specs.operator(4,1,'-') == 3, "Opertator failed for subtraction"
    assert specs.operator(4,1,'*') == 4, "Opertator failed for multiplication"


# Finishes testing the complex number class
@pytest.fixture
def set_up_complex_nums():
    number_1 = specs.ComplexNumber(1, 2)
    number_2 = specs.ComplexNumber(5, 5)
    number_3 = specs.ComplexNumber(2, 9)
    return number_1, number_2, number_3

def test_complex_addition(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 + number_2 == specs.ComplexNumber(6, 7)
    assert number_1 + number_3 == specs.ComplexNumber(3, 11)
    assert number_2 + number_3 == specs.ComplexNumber(7, 14)
    assert number_3 + number_3 == specs.ComplexNumber(4, 18)

def test_complex_multiplication(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 * number_2 == specs.ComplexNumber(-5, 15)
    assert number_1 * number_3 == specs.ComplexNumber(-16, 13)
    assert number_2 * number_3 == specs.ComplexNumber(-35, 55)
    assert number_3 * number_3 == specs.ComplexNumber(-77, 36)

def test_complex_subtraction(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 - number_2 == specs.ComplexNumber(-4, -3)
    assert number_1 - number_3 == specs.ComplexNumber(-1, -7)
    assert number_2 - number_3 == specs.ComplexNumber(3, -4)
    assert number_3 - number_3 == specs.ComplexNumber(0, 0)

def test_complex_division(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 / number_2 == specs.ComplexNumber(.3, .1)
    assert number_1 / number_3 == specs.ComplexNumber(20./85, -5./85)
    assert number_2 / number_3 == specs.ComplexNumber(55./85, -35./85)
    assert number_3 / number_3 == specs.ComplexNumber(1, 0)

    with pytest.raises(Exception) as excinfo:
        number_1 / specs.ComplexNumber()
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Cannot divide by zero"

def test_complex_equal(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert (number_1 == number_1) == True
    assert (number_1 == number_2) == False

def test_complex_string(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert str(number_1) == "1+2i"

def test_complex_norm(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1.norm() == math.sqrt(5)

# test cases for the Set game.

def test_setgame():

    with pytest.raises(Exception) as excinfo:
        specs.findsets(filename="Hands/Hand_duplicate.txt")
    assert excinfo.typename == 'ValueError'#??
    assert excinfo.value.args[0] == "Invalid Set: Duplicate Card"

    with pytest.raises(Exception) as excinfo:
        specs.findsets(filename="Hands/Hand_invalid_card.txt")
    assert excinfo.typename == 'ValueError'#??
    assert excinfo.value.args[0] == "Invalid Set: Invalid Card length"

    with pytest.raises(Exception) as excinfo:
        specs.findsets(filename="Hands/Hand_invalid_card2.txt")
    assert excinfo.typename == 'ValueError'#??
    assert excinfo.value.args[0] == "Invalid Set: Invalid Card number"

    with pytest.raises(Exception) as excinfo:
        specs.findsets(filename="Hands/Hand_extra.txt")
    assert excinfo.typename == 'ValueError'#??
    assert excinfo.value.args[0] == "Invalid Set: Wrong ammount of cards"

    with pytest.raises(Exception) as excinfo:
        specs.findsets(filename="Hands/Hand_too_few.txt")
    assert excinfo.typename == 'ValueError'#??
    assert excinfo.value.args[0] == "Invalid Set: Wrong ammount of cards"

    assert specs.findsets(filename="Hands/Hand_good.txt") == 7, "findsets failed for Hand_good.txt"
