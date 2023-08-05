class HuoYanError(Exception):
    """nothing"""


def _raise_huoyanerror_object():
    raise HuoYanError('Please use the right object')


__version__ = '1.1.3'
__author__ = 'F.S'
__thank__ = ['Bingyi Liu']
