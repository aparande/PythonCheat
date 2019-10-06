import random
import string
import os

def randomString(stringLength=10):
    """
    Generate a random string of fixed length 
    https://pynative.com/python-generate-random-string/
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def clearScreen():
    os.system("clear")