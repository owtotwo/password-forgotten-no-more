#!/usr/bin/env python

"""
    A tool to generate an random account username and strong password by your 
common password. 
    If you provide a website name or a username (just keep the Website input 
empty), and your common password, the corresponding strong password will remind
you accurately. The username will always give you, don't worry about forgetting.
    If you only provide your common password, you will get a random username
and a strong password.
    P.S. The strong password is NOT contain the space character.
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

__version__ = "0.0.1"

import hashlib
import time
import urlparse
import random

USERNAME_LENGTH = 10
PASSWORD_LENGTH = 16

is_account_generator = False

website = raw_input("Website(salt/empty):")
username = ''
if not website:
    username = raw_input("Username(salt/empty):")
else:
    parsed_uri = urlparse.urlparse(website)
    if parsed_uri.netloc:
        website = parsed_uri.netloc
    website = website.lower()
    md5 = hashlib.md5()
    md5.update(website)
    hash_website = md5.hexdigest()
    username = hash_website[:USERNAME_LENGTH]

if not username:
    is_account_generator = True
    timestamp = time.time()
    random_float = random.SystemRandom().random()
    md5 = hashlib.md5()
    md5.update(str(timestamp + random_float))
    username = md5.hexdigest()[:USERNAME_LENGTH]

password = raw_input("Password:")

if not password:
    print("Error: Password cannot be empty.")
    exit()

pwd_str = password

if username:
    md5 = hashlib.md5()
    md5.update(username)
    pwd_str = pwd_str + md5.hexdigest()
    
sha1 = hashlib.sha1()
sha1.update(pwd_str)
cipher = sha1.hexdigest()


if not cipher.isalnum():
    print("Error: Input String is not Alphabet or Number.")
    exit()

ascii_list = []

DIGIT_NUM = ord('9') - ord('0') + 1
UPPERCASE_NUM = ord('Z') - ord('A') + 1
LOWERCASE_NUM = ord('z') - ord('a') + 1
MD5_BASE = DIGIT_NUM + UPPERCASE_NUM + LOWERCASE_NUM

for c in cipher:
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

passwd_str = ''.join([ chr(n + BEGIN_ASCII_NUM) for n in new_ascii_list ])

password = passwd_str[:PASSWORD_LENGTH]

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
