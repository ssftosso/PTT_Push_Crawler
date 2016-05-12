# -*- coding: utf8 -*-
import __init__
import time
from config import *
from lib import MessageHandler
import os

## Push
class Push:
    Type        = ''
    Account     = ''
    Content     = ''
    Time        = ''
    Title       = ''
    Board       = ''

    def __init__(self, Type='',\
                 Account='',\
                 Content='',\
                 Time='',\
                 Title='',\
                 Board=''):
        self.Type       = Type
        self.Account    = Account
        self.Content    = Content
        self.Time       = Time
        self.Title      = Title
        self.Board      = Board

    def show(self):
        print "[" + self.Time + \
              "] [" + self.Board +\
              "] [" + self.Title +\
              "] [" + self.Type +\
              "] [" + self.Account +\
              "]: " + self.Content

# Target
class Target:
    URL = ''
    BoardName = ''

    def __init__(self, URL, BoardName=None):
        self.URL = URL
        self.BoardName = BoardName
        

# Connector error 
class ConnectError:
    Count = 0
    
    def __init__(self, Count = 0):
        self.Count = Count

    def Delay(self):
        # Reconnect by 2^N seconds
        DelayTime = 2**self.Count
        if DelayTime == 0:
            DelayTime = 2
        ErrorLog("ErrorCount=" + str(self.Count) + " & Delaytime=" + str(DelayTime), "ConnectError")
        time.sleep(config.DelayTime)


def DelayError(Error):
    if Error != None:
        Error.Delay()
        Error.Count = Error.Count + 1
        return Error
    else:
        Error = ConnectError(Count = 1)
        return Error

def Delay(delaytime):
    time.sleep(delaytime)   

    
