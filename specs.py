# specs.py
"""Testing.
Bailey Smith
January 4 2017
"""
import math

# Problem 1 Write unit tests for addition().
# Be sure to install pytest-cov in order to see your code coverage change.
def addition(a,b):
    return a + b

def smallest_factor(n):
    """Finds the smallest prime factor of a number.
    Assume n is a positive integer.
    """
    if n == 1:
        return 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return i
    return n


# Unit tests for operator().
def operator(a, b, oper):
    if type(oper) != str:
        raise ValueError("Oper should be a string")
    if len(oper) != 1:
        raise ValueError("Oper should be one character")
    if oper == "+":
        return a+b
    if oper == "/":
        if b == 0:
            raise ValueError("You can't divide by zero!")
        return a/float(b)
    if oper == "-":
        return a-b
    if oper == "*":
        return a*b
    else:
        raise ValueError("Oper can only be: '+', '/', '-', or '*'")

# Unit test for this class.
class ComplexNumber(object):
    def __init__(self, real=0, imag=0):
        self.real = real
        self.imag = imag

    def conjugate(self):
        return ComplexNumber(self.real, -self.imag)

    def norm(self):
        return math.sqrt(self.real**2 + self.imag**2)

    def __add__(self, other):
        real = self.real + other.real
        imag = self.imag + other.imag
        return ComplexNumber(real, imag)

    def __sub__(self, other):
        real = self.real - other.real
        imag = self.imag - other.imag
        return ComplexNumber(real, imag)

    def __mul__(self, other):
        real = self.real*other.real - self.imag*other.imag
        imag = self.imag*other.real + other.imag*self.real
        return ComplexNumber(real, imag)

    def __div__(self, other):
        if other.real == 0 and other.imag == 0:
            raise ValueError("Cannot divide by zero")
        bottom = (other.conjugate()*other*1.).real
        top = self*other.conjugate()
        return ComplexNumber(top.real / bottom, top.imag / bottom)

    def __eq__(self, other):
        return self.imag == other.imag and self.real == other.real

    def __str__(self):
        return "{}{}{}i".format(self.real, '+' if self.imag >= 0 else '-',
                                                                abs(self.imag))

# Code for the Set game here
def findsets(filename="Hands/Hand_good.txt"):
    '''Read in file, if fails raise error'''
    lines = []
    with open(filename, 'r') as myfile:
        for line in myfile:
            line = line.strip()
            for i in line:
                if i != '0' and i != '1' and i != '2':
                    raise ValueError("Invalid Set: Invalid Card number")
            if len(line) != 4:
                raise ValueError("Invalid Set: Invalid Card length")
            if line in lines:
                raise ValueError("Invalid Set: Duplicate Card")
            lines.append(line)
        if len(lines) != 12:
            raise ValueError("Invalid Set: Wrong ammount of cards")

    '''triple for loop, '''
    count = 0
    for i in xrange(10):
        for a in xrange(i+1,11):
            for b in xrange(a+1,12):
                sum1 = int(lines[i][0]) + int(lines[a][0]) + int(lines[b][0])
                sum2 = int(lines[i][1]) + int(lines[a][1]) + int(lines[b][1])
                sum3 = int(lines[i][2]) + int(lines[a][2]) + int(lines[b][2])
                sum4 = int(lines[i][3]) + int(lines[a][3]) + int(lines[b][3])
                if sum1 % 3 == 0 and sum2 % 3 == 0 and sum3 % 3 == 0 and sum4 % 3 == 0:
                    count += 1
    return count
