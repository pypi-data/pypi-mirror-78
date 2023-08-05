from time import *
from huoyanlib import _raise_huoyanerror_object


def clean(t):
    import sys
    try:
        t = int(t)
        sleep(t)
    except ValueError:
        _raise_huoyanerror_object()
    sys.stdout.write('\033[2J\033[00H')


def clear():
    import sys
    sys.stdout.write('\033[2J\033[00H')
