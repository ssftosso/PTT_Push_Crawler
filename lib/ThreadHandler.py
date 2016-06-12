# -*- coding: utf8 -*-
import __init__ 
from config import *
from item import *
from MessageHandler import *
from WebHandler import *
from Downloader import *

import threading, thread
import Queue

 

class DownloadPushThread(threading.Thread):
    def __init__(self, target, threadID):
        threading.Thread.__init__(self)
        self.threadID   = threadID
        self.target     = target

    def run(self):
        RunningLog(message = "Starting thread[{:}]".format(self.threadID), module = "DownloadPushThread", level=4)

        try:
            DownloadPush(self.target)
        except Exception:
            ErrorLog("Restart run(self)","Class.DownloadPushThread")
            run(self)
        
        RunningLog(message = "Stop thread[{:}]".format(self.threadID), module = "DownloadPushThread", level=4)

def StartDownloadPushThread(target, threadID=0):
    try:
        mthread = DownloadPushThread(target, threadID)
        mthread.start()
    except Exception:
        ErrorLog("Restart, target.URL={:}".format(target.URL),"StartDownloadPushThread")
        StartDownloadPushThread(target, threadID)


def ShowThreadCount():
    print "test={:}".format(threading.active_count())


def GetThreadCount():
    result = 0 
    try:
        result = threading.active_count()
    except Exception:
        ErrorLog("Get num of thread fail and set to 0","GetThreadCount")
    return result

def GetDownloadThreadCount(BasicThreadCount):
    # For checking the thread used for download push
    result = GetThreadCount() - BasicThreadCount
    return result
    
