"""For demonstration and testing purposes."""

print(__doc__ + '\n')

import re

import ykpstools as yt


# Create a user. ('prompt' means to prompt for username and password in python
#                 shell if not available.)
user = yt.User(prompt=True)

# YKPS site Wi-Fi authorization
try:
    user.auth()
except yt.Error as error:
    print("Can't log in to school Wi-Fi.\n")

# Login to Powerschool Learning
powerschool_learning = user.psl_login().soup()
true_name = powerschool_learning.find('div', id='navbarowner').string.strip()
print('Hello, {}.\n'.format(true_name))

# Login to Powerschool (here I use html.parser because lxml has wierd issues)
powerschool = user.ps_login().soup(features='html.parser')

# Parse all the class names and grades (code looks a bit complicated...)
classes, names, grades = zip(*[
    (
        tr,
        tr.find('td', align='left').get_text(),
        ord(tr.find('a', class_='bold').string[0]),
    )
    for tr in powerschool.find_all('tr', id=re.compile(r'ccid_[0-9]{6}'))
    if (tr.find('a', class_='bold') is not None
        and tr.find('a', class_='bold').string[0].isalpha())
])

# Lowest score (ouch!)
lowest = grades.index(max(grades)) # max(ord) b/c e.g. ord('E') > ord('A')
print('Your class with lowest score is: {}.\n'.format(names[lowest]))
print('Score: {}'.format(classes[lowest].find('a', class_='bold').string))