class HuoYanError(Exception):
    """nothing"""


def _raise_huoyanerror_object():
    raise HuoYanError('Please use the right object')


def _raise_huoyanerror_parameter():
    raise HuoYanError('All parameters you pass in must have default values')


__version__ = '1.4.3'
__author__ = 'F.S'
__thank__ = ['Bingyi Liu', 'Ziyv Yan', 'Zeyv Zhong']
