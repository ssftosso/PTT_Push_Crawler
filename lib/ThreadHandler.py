# -*- coding: utf8 -*-
import __init__ 
from config import *
from item import *
from MessageHandler import *
from WebHandler import *

import threading, thread
import Queue


class DownloadPushThread(threading.Thread):
    def __init__(self, threadID, target):
        threading.Thread.__init__(self)
        self.threadID   = threadID
        self.target     = target

    def run(self):
        RunningLog(message = "Starting thread[{:}]".format(self.threadID), module = "DownloadPushThread", level=4)

        try:
            DownloadPush(self.target)
        except:
            ErrorLog("Restart run(self)","Class.DownloadPushThread")
            run(self)
        
        RunningLog(message = "Stop thread[{:}]".format(self.threadID), module = "DownloadPushThread", level=4)

def StartDownloadPushThread(threadID, target):
    try:
        mthread = DownloadPushThread(threadID, target)
        mthread.start()
    except:
        ErrorLog("Restart, target.URL={:}".format(target.URL),"StartDownloadPushThread")
        StartDownloadPushThread(threadID, target)
    

def ShowThreadCount():
    print "test={:}".format(threading.active_count())


def GetThreadCount():
    result = 0 
    try:
        result = threading.active_count()
    except:
        ErrorLog("Get num of thread fail and set to 0","GetThreadCount")
    return result

def GetDownloadThreadCount(BasicThreadCount):
    # For checking the thread used for download push
    result = GetThreadCount() - BasicThreadCount
    return result
    
