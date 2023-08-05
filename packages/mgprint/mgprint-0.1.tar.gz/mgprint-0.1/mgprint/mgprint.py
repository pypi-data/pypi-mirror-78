import re
import os
from sys import stdout


def mstr(string):
    colors = {
            # Colors
            "r": "[31m", "g": "[32m",
            "y": "[33m", "b": "[34m",
            "m": "[35m", "c": "[36m",
            "w": "[37m", "0": "[30m",
            # Backgrounds
            "R": "[41;1m", "G": "[42;1m", "#": "[40;1m",
            "Y": "[43;1m", "B": "[44;1m", "M": "[45;1m",
            "C": "[46;1m", "W": "[47;1m",
            # Styles
            "*": "[1m",
            "_": "[4m",
            "-": "[7m",

            ";": "[0m"  # Reset
        }
    alphab = ''.join(list(colors.keys()))
    for c in alphab:
        if not c.isalnum():
            alphab = alphab.replace(c, chr(92) + c)
    if type(string) == str:
        ret = re.findall(
            r"%[{alph}]+?%|&[{alph}]+?&"
            .format(alph=alphab), string, re.MULTILINE
            )
        for match in ret:
            aux = ""
            for j in match[1:-1]:
                if(list(colors.keys()).count(j) != 0):
                    aux += "\033"+colors[j]
            string = string.replace(match, aux)
    return string


def mprint(string, strict=False):
    print(mstr(string) + ("", "\033[0m")[not strict])


def cprint(string, strict=False):
    stdout.write(mstr(string) + ("", "\033[0m")[not strict])


def mreset():
    stdout.write("\033[0m")


def printHead(string, dim=40):
    if len(string) <= dim:
        mprint("%-*%" + "{0}".format(string.upper()).center(dim))
    else:
        mprint("%-*%{0}...%;%".format(string.upper()[0:dim-3]))


def cls():
    os.system(("cls", "clear")[os.name != 'nt'])
