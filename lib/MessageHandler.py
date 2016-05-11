# -*- coding: utf8 -*-
import __init__ 
from config import *


def LogType(logtype):
    mes = "[{:^7}] ".format(logtype)
    return mes

def RunningLog(message, level= 5, module = None):
    # level
    #  top: 0
    # down: 5 (default)
    
    mes = LogType("LOG")
    if module != None:
        mes = mes + "[" + module + "]"
    mes = mes + message

    if level <= RunningLogLevel:
        print mes


def ErrorLog(message, module = None):
    mes = LogType("ERROR")
    if module != None:
        mes = mes + "[" + module + "]"
    mes = mes + message
    print mes

