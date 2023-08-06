
from termcolor import colored, cprint

def greenp(text, t=0, n=0):
    print("\t" * t, end='')
    cprint(text, 'green', end='')
    print("\n" * n, end='')

def cyanp(text, t=0, n=0):
    print("\t" * t, end='')
    cprint(text, 'cyan', end='')
    print("\n" * n, end='')

def whitep(text, t=0, n=0):
    print("\t" * t, end='')
    cprint(text, 'white', end='')
    print("\n" * n, end='')

def yellowp(text, t=0, n=0):
    print("\t" * t, end='')
    cprint(text, 'yellow', end='')
    print("\n" * n, end='')

def redp(text, t=0, n=0):
    print("\t" * t, end='')
    cprint(text, 'red', end='')
    print("\n" * n, end='')

def defaultp(text, t=0, n=0):
    print("\t" * t, end='')
    print(text, end='')
    print("\n" * n, end='')

def boldp(text, t=0, n=0):
    print("\t" * t, end='')
    cprint(text, attrs=['bold'], end='')
    print("\n" * n, end='')

def br(num=1):
    print("\n" * num, end='')


def keyvaluep(text1, text2, color2=None, color1=None, t=0, n=0):
    print("\t" * t, end='')
    if color1:
        cprint(text1, color1, end='')
    else:
        print(text1, end='')

    if color2:
        cprint(text2, color2, end='')
    else:
        print(text2, end='')

    print("\n" * n, end='')
