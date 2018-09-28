"""Introduction to BeautifulSoup.
Bailey Smith
September 28 2017
"""

import re
import codecs
import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

# Example HTML string from the lab.
pig_html = """
<html><head><title>Three Little Pigs</title></head>
<body>
<p class="title"><b>The Three Little Pigs</b></p>
<p class="story">Once upon a time, there were three little pigs named
<a href="http://example.com/larry" class="pig" id="link1">Larry,</a>
<a href="http://example.com/mo" class="pig" id="link2">Mo</a>, and
<a href="http://example.com/curly" class="pig" id="link3">Curly.</a>
<p>The three pigs had an odd fascination with experimental construction.</p>
<p>...</p>
</body></html>
"""


def prob1():
    """Examine the source code of http://www.example.com. Determine the names
    of the tags in the code and the value of the 'type' attribute associated
    with the 'style' tag.

    Returns:
        (set): A set of strings, each of which is the name of a tag.
        (str): The value of the 'type' attribute in the 'style' tag.
    """

    setOfTags = set(["html", "head", "title", "meta", "style", "body", "div", "h1", "p", "a"])
    return(setOfTags,"text/css")

# Problem 2
def prob2(code):
    """Return a list of the names of the tags in the given HTML code."""
    soup = BeautifulSoup(code, 'html.parser')
    return [tag.name for tag in soup.find_all(True)]

# Problem 3
def prob3(filename="example.html"):
    """Read the specified file and load it into BeautifulSoup. Find the only
    <a> tag with a hyperlink and return its text.
    """

    data = codecs.open(filename,"r")
    soup = BeautifulSoup(data, 'html.parser')
    if "href" in soup.a.attrs:
        return soup.a.get_text().strip()


# Problem 4
def prob4(filename="san_diego_weather.html"):
    """Read the specified file and load it into BeautifulSoup. Return a list
    of the following tags:

    1. The tag containing the date 'Thursday, January 1, 2015'.
    2. The tags which contain the links 'Previous Day' and 'Next Day'.
    3. The tag which contains the number associated with the Actual Max
        Temperature.

    Returns:
        (list) A list of bs4.element.Tag objects (NOT text).
    """
    listOfTags = []
    data = codecs.open(filename,"r")
    soup = BeautifulSoup(data, 'html.parser')

    listOfTags.append(soup.find(string='Thursday, January 1, 2015').parent)
    listOfTags.append(soup.find(attrs={"class": "previous-link"}))
    listOfTags.append(soup.find(attrs={"class": "next-link"}))
    listOfTags.append(soup.find(string='59').parent)

    return(listOfTags)



# Problem 5
def prob5(filename="large_banks_index.html"):
    """Read the specified file and load it into BeautifulSoup. Return a list
    of the tags containing the links to bank data from September 30, 2003 to
    December 31, 2014, where the dates are in reverse chronological order.

    Returns:
        (list): A list of bs4.element.Tag objects (NOT text).
    """
    data = codecs.open(filename,"r")
    soup = BeautifulSoup(data, 'html.parser')
    tags = [tag.parent for tag in soup.find_all(string=re.compile(r"^[A-Z][a-z]+ 3[01], 20((0[3-9])|1[0-4])$"))]
    return tags[:-1]



# Problem 6
def prob6(filename="large_banks_data.html"):
    """Read the specified file and load it into BeautifulSoup. Create a single
    figure with two subplots:

    1. A sorted bar chart of the seven banks with the most domestic branches.
    2. A sorted bar chart of the seven banks with the most foreign branches.

    In the case of a tie, sort the banks alphabetically by name.
    """
    banknames = []
    domestic = []
    foreign = []
    data = codecs.open(filename,"r")
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find(name='table')
    body = table.find('tbody')
    rows = [tag for tag in body.find_all('tr')]#don't need list comprehension
    pattern = re.compile(r"([0-9]),?((?:[0-9])*)")

    for row in rows:
        cols = [tag.text.strip() for tag in row.find_all('td')]
        if cols[9] != '.':
            banknames.append(cols[0])
            domestic.append(int(pattern.sub(r"\1\2", cols[9])))
            foreign.append(int(pattern.sub(r"\1\2", cols[10])))

    index_domestic = np.argsort(domestic)[::-1]
    index_foreign = np.argsort(foreign)[::-1]
    sort_domestic = np.array(domestic)[index_domestic][:7]
    bank_domestic = np.array(banknames)[index_domestic][:7]
    sort_foreign = np.array(foreign)[index_foreign][:7]
    bank_foreign = np.array(banknames)[index_foreign][:7]
    temp = bank_foreign[5]
    bank_foreign[5] = bank_foreign[6]
    bank_foreign[6] = temp

    y_pos = np.arange(7)

    plt.subplot(211)
    plt.title('Domestic')
    plt.barh(y_pos,sort_domestic,align='center',alpha=0.5)
    plt.xlim(0,5000)
    plt.yticks(y_pos, bank_domestic, fontsize=6)

    plt.subplot(212)
    plt.title('Foreign')
    plt.barh(y_pos,sort_foreign,align='center',alpha=0.5)
    plt.xlim(0,5000)
    plt.yticks(y_pos, bank_foreign, fontsize=6)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    code = """<!doctype html>
<html>
<head>
    <title>Example Domain</title>

    <meta charset="utf-8" />
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style type="text/css">
    body {
        background-color: #f0f0f2;
        margin: 0;
        padding: 0;
        font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;

    }
    div {
        width: 600px;
        margin: 5em auto;
        padding: 50px;
        background-color: #fff;
        border-radius: 1em;
    }
    a:link, a:visited {
        color: #38488f;
        text-decoration: none;
    }
    @media (max-width: 700px) {
        body {
            background-color: #fff;
        }
        div {
            width: auto;
            margin: 0 auto;
            border-radius: 0;
            padding: 1em;
        }
    }
    </style>
</head>

<body>
<div>
    <h1>Example Domain</h1>
    <p>This domain is established to be used for illustrative examples in documents. You may use this
    domain in examples without prior coordination or asking for permission.</p>
    <p><a href="http://www.iana.org/domains/example">More information...</a></p>
</div>
</body>
</html>
"""
    print(prob5())
    # print(prob6())

    pass
