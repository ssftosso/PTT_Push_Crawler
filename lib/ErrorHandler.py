# -*- coding: utf8 -*-
import __init__ 
from config import *
from item import *
from MessageHandler import *

import time

def Delay(delaytime):
    time.sleep(delaytime)
    RunningLog("Delay {:} seconds".format(delaytime),"ErrorHandler.Delay")
    
