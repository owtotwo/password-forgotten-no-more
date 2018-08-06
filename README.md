# password-forgotten-no-more (v2)
An account and password generator, a password reminder as well.

## Update
**Update on 2018/8/6. More Safe.**

In order to prevent brute force, the v2 do more hash rounds to increase the consumption of computing resource.

For keeping the weight light, it has not use the bcrypt. That is, without any dependencies but python standard library.

**If you had use it at some time in the past, you should find the old version ([v1](https://github.com/owtotwo/password-forgotten-no-more/tree/v1)) to use.**

## Usage
`> python2 pwd_4goten_no_more.py`

If you provide a website name or a username (just keep the Website input 
empty), and your common password, the corresponding strong password will remind
you accurately. The username will always give you, don't worry about forgetting.

If you only provide your common password, you will get a random username
and a strong password.

P.S. The strong password is NOT contain the space character. And Website
Name supports Unicode (e.g. zh-cn).

## Requirements
Python 2 (version 2.5 or later). (Python 3 does not support at the moment.)
