from huoyanlib import _raise_huoyanerror_object


colors = [31, 32, 33, 34, 35, 36, 37, 91, 92, 93, 94, 95, 96, 97]


def spark(word, time_of_spark):
    import random
    import time
    import sys
    try:
        times = int(time_of_spark / 0.1)
    except ValueError:
        _raise_huoyanerror_object()
    try:
        for i in range(times):
            print("\033[{}m{}".format(random.choice(colors), word))
            time.sleep(0.1)
            sys.stdout.write('\033[2J\033[00H')
    except UnboundLocalError:
        _raise_huoyanerror_object()
