from sys import*
from time import*
from os import*
def print_one_by_one(text,time):
    stdout.write("\r " + " " * 60 + "\r")
    stdout.flush()
    for c in text:
        stdout.write(c)
        stdout.flush()
        sleep(time)


