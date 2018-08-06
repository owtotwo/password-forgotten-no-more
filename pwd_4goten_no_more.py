#!/usr/bin/env python

"""
    A tool to generate an random account username and strong password by your 
common password. 
    If you provide a website name or a username (just keep the Website input 
empty), and your common password, the corresponding strong password will remind
you accurately. The username will always give you, don't worry about forgetting.
    If you only provide your common password, you will get a random username
and a strong password.
    P.S. The strong password is NOT contain the space character. And Website
Name supports Unicode (e.g. zh-cn).
"""

# Copyright (c) 2018, owtotwo.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

__version__ = "0.2.0"

import hashlib
import time
import urlparse
import random
import re

def alphanum_to_alphanumpunct(s):
    assert s.isalnum()
    ascii_list = []

    DIGIT_NUM = ord('9') - ord('0') + 1
    UPPERCASE_NUM = ord('Z') - ord('A') + 1
    LOWERCASE_NUM = ord('z') - ord('a') + 1
    MD5_BASE = DIGIT_NUM + UPPERCASE_NUM + LOWERCASE_NUM

    for c in s:
        if c.isdigit():
            ascii_list.append(ord(c) - ord('0'))
        elif c.isupper():
            ascii_list.append(ord(c) - ord('A') + DIGIT_NUM)
        elif c.islower():
            ascii_list.append(ord(c) - ord('a') + DIGIT_NUM + UPPERCASE_NUM)
        else:
            raise Exception()

    ascii_list.reverse()

    sum = 0

    for i, n in enumerate(ascii_list):
        sum = sum + n * (MD5_BASE ** i)

    BEGIN_ASCII_NUM = ord('!') # space not allowed
    PASSWD_BASE = ord('~') - BEGIN_ASCII_NUM + 1

    new_ascii_list = [] # with punctution

    while sum > 0:
        new_ascii_list.append(sum % PASSWD_BASE)
        sum = sum // PASSWD_BASE

    new_ascii_list.reverse()
    return ''.join([ chr(n + BEGIN_ASCII_NUM) for n in new_ascii_list ])


def hashsum(hash):
    def temp(s):
        assert s
        _hash = hash()
        _hash.update(s)
        return _hash.hexdigest()
    return temp

def hashsum_many_times(hash):
    _hashsum = hashsum(hash)
    def temp(s, times):
        _sum = s
        for _ in range(times):
            _sum = _hashsum(_sum)
        return _sum
    return temp

md5sum = hashsum(hashlib.md5)
sha1sum = hashsum(hashlib.sha1)
sha1sum_many_times = hashsum_many_times(hashlib.sha1)

def is_strong_password(s):
    result = re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[][!"#$%&\'()*+,./:;<=>?@\\^_`{|}~-])[\x21-\x7E]{8,}$', s)
    # print('"' + s + '"' + (' Yes!' if result else ' No!'))
    return result


USERNAME_LENGTH = 10
PASSWORD_LENGTH = 16
SHA1SUM_TIMES = 777777 # To EDG.clearlove

is_account_generator = False

website = raw_input("Website(salt/empty):")
username = '' if website else raw_input("Username(salt/empty):")
password = raw_input("Password:")

if not password:
    print("Error: Password cannot be empty.")
    exit()

if website and not username:
    # maybe it is a url of website.
    parsed_uri = urlparse.urlparse(website)
    if parsed_uri.netloc:
        website = parsed_uri.netloc
    website = website.lower()
    username = md5sum(website + password)[:USERNAME_LENGTH]
elif not website and not username:
    is_account_generator = True
    timestamp = time.time()
    random_float = random.SystemRandom().random()
    username = md5sum(str(timestamp + random_float))[:USERNAME_LENGTH]

cipher = sha1sum_many_times(password + md5sum(username), SHA1SUM_TIMES)
password = alphanum_to_alphanumpunct(cipher)[:PASSWORD_LENGTH]
while not is_strong_password(password):
    cipher = sha1sum(cipher)
    password = alphanum_to_alphanumpunct(cipher)[:PASSWORD_LENGTH]


print("\n")
if is_account_generator:
    print("Generating...")
else:
    print("Find account information...")
print("Successfully!")
print("----------------------------------")
print(" Username: " + username)
print(" Password: " + password)
print("----------------------------------")
