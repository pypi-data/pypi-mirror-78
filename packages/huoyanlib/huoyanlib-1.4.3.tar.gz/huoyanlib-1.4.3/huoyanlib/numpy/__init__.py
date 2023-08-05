class HNumPyError(Exception):
    """nothing"""


def _raise_hnumpyerror_int_str():
    raise HNumPyError("object error:please use type \'int\'(not \'str\')")