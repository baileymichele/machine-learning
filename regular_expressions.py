# regular_expressions.py
"""Regular Expressions.
Bailey Smith
September 14 2017
"""
import re

def example1():
    """Compile and return a regular expression pattern object with the
    pattern string "python".

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    pattern = re.compile("python")
    return pattern

def example2():
    """Compile and return a regular expression pattern object that matches
    the string "^{@}(?)[%]{.}(*)[_]{&}$".

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    pattern = re.compile(r"\^\{@\}\(\?\)\[%\]\{\.\}\(\*\)\[_\]\{&\}\$")
    return pattern

def example3():
    """Compile and return a regular expression pattern object that matches
    the following strings (and no other strings).

        Book store          Mattress store          Grocery store
        Book supplier       Mattress supplier       Grocery supplier

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    pattern = re.compile(r"^(Book|Mattress|Grocery) (store|supplier)$")
    return pattern


def example4():
    """Compile and return a regular expression pattern object that matches
    any valid Python identifier.

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    pattern = re.compile(r"^(_|[a-zA-Z])(_|\w)*$")
    return pattern


def example5(code):
    """Use regular expressions to place colons in the appropriate spots of the
    input string, representing Python code. You may assume that every possible
    colon is missing in the input string.

    Parameters:
        code (str): a string of Python code without any colons.

    Returns:
        (str): code, but with the colons inserted in the right places.
    """
    pattern = re.compile(r"^(\s*(?:if|elif|for|while|try|with|def|class|finally|else|except)(?: .+)?)\n",re.MULTILINE)
    #using re.VERBOSE you can write the regular_expression on different lines and comment on each piece
    return pattern.sub(r"\1:\n", code)


def example6(filname="fake_contacts.txt"):
    """Use regular expressions to parse the data in the given file and format
    it uniformly, writing birthdays as mm/dd/yyyy and phone numbers as
    (xxx)xxx-xxxx. Construct a dictionary where the key is the name of an
    individual and the value is another dictionary containing their
    information. Each of these inner dictionaries should have the keys
    "birthday", "email", and "phone". In the case of missing data, map the key
    to None.

    Returns:
        (dict): a dictionary mapping names to a dictionary of personal info.
    """
    #everything before the @ without @
    '''a = compile(r".*(?=!)")
    a.findall("hey there!")
    gives ["hey there"]'''

    contacts = {}
    name = re.compile(r"^([A-Za-z]* (?:[A-Z]\. )?[A-Za-z]+)")#?: means non capturing
    birthday = re.compile(r"([0-1]?[\d])/([0-3]?[\d])/((?:\d\d)(?:\d\d)?)")
    email = re.compile(r"[\w\.]+@[\w\.]+\.[a-z]{3}")
    phone = re.compile(r"(?:1-)?\(?(\d{3})\)?(\d{3})-?(\d{4})")
    with open(filname, 'r') as f:
        for line in f:
            # print(email.findall(line))
            newName = name.findall(line)[0]
            contacts[newName] = {'birthday': None, 'email': None, 'phone': None}
            birth = birthday.findall(line)
            e = email.findall(line)
            p = phone.findall(line)
            if birth:
                a,b,c = birth[0]
                if len(a) == 1:
                    a = "0" + a
                if len(b) == 1:
                    b = "0" + b
                if len(c) == 2:
                    c = "20" + c
                newBirthday = a + "/" + b + "/" + c
                contacts[newName]['birthday'] = newBirthday
            if e:
                contacts[newName]['email'] = e[0]
            if p:
                a,b,c = p[0]
                contacts[newName]['phone'] = "({}){}-{}".format(a,b,c)

    return contacts




def test1():
    pattern = example1()
    positive = ["python", "python3", "python2.7", "your python ran away"]
    assert all(pattern.search(p) for p in positive)
    negative = ["py2thon", "ython3", "thon2.7py", "your pytho ran away"]
    assert not any(pattern.search(n) for n in negative)
    return True

def test2():
    pattern = example2()
    positive = ["^{@}(?)[%]{.}(*)[_]{&}$", "pyt^{@}(?)[%]{.}(*)[_]{&}$hon", "python3^{@}(?)[%]{.}(*)[_]{&}$", "^{@}(?)[%]{.}(*)[_]{&}$python2.7"]
    assert all(pattern.search(p) for p in positive)
    negative = [" ", "py2thon", "^{@}(?)[%]{.}", "(*)[_]{&}$", "^{@}(?)[%]{.}(*)[_]{&}"]
    assert not any(pattern.search(n) for n in negative)
    return True

def test3():
    pattern = example3()
    positive = ["Book store", "Mattress store", "Grocery store", "Book supplier", "Mattress supplier", "Grocery supplier"]
    assert all(pattern.search(p) for p in positive)
    negative = ["Book store ", "Book store Mattress store", "Grocery", "Mattresssupplier"]
    assert not any(pattern.search(n) for n in negative)
    return True

def test4():
    pattern = example4()
    positive = ["Mouse", "compile", "_123456789", "__x__", "while"]
    assert all(pattern.search(p) for p in positive)
    negative = ["3rats", "err*r", "sq(x)", "sleep()", " x"]
    assert not any(pattern.search(n) for n in negative)
    return True

def test5():
    code = """
 k, i, p = 999, 1, 0
 while k > i
     i *= 2
     p += 1
     if k != 999
         print("k should not have changed")
     else
         pass
 print(p)
"""
    return example5(code)

if __name__ == '__main__':
    # print(test1())
    # print(test2())
    # print(test3())
    # print(test4())
    # print(test5())
    print(example6())
