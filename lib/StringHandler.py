# -*- coding: utf8 -*-
import __init__ 
from config import *
from item import *
from MessageHandler import *


def ArrayInto1String(array):
    result = ''
    try:
        for item in array:
            result = result + item
    except:
        ErrorLog("Combine into one string fail","ArrayInto1String")

        
    return result

