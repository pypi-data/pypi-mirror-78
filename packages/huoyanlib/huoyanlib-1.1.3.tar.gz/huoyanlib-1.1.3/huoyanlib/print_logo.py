"""
字体色     |      背景色      |      颜色描述
-------------------------------------------
30        |        40       |      d黑色
31        |        41       |      r红色
32        |        42       |      g绿色
33        |        43       |      y黃色
34        |        44       |      b蓝色
35        |        45       |      p紫红色
36        |        46       |      q青蓝色
37        |        47       |      w白色
-------------------------------------------
参考文献：https://www.cnblogs.com/daofaziran/p/9015284.html
"""


def logo(a):
    for x in range(len(a)):
        if a[x] == "0":
            print("\033[40m ", end="")
        elif a[x] == "1":
            print("\033[41m ", end="")
        elif a[x] == "2":
            print("\033[42m ", end="")
        elif a[x] == "3":
            print("\033[43m ", end="")
        elif a[x] == "4":
            print("\033[44m ", end="")
        elif a[x] == "5":
            print("\033[45m ", end="")
        elif a[x] == "6":
            print("\033[46m ", end="")
        elif a[x] == "7":
            print("\033[47m ", end="")
        elif a[x] == "d":
            print("\033[30m ", end='')
        elif a[x] == "r":
            print("\033[31m ", end="")
        elif a[x] == "g":
            print("\033[32m ", end="")
        elif a[x] == "y":
            print("\033[33m ", end="")
        elif a[x] == "b":
            print("\033[34m ", end="")
        elif a[x] == "p":
            print("\033[35m ", end="")
        elif a[x] == "q":
            print("\033[36m ", end="")
        elif a[x] == "w":
            print("\033[37m ", end="")
        else:
            print(a[x], end="")
    print("\033[0m")
