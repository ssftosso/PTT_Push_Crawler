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
        self.threadID = threadID
        self.target = target

    def run(self):
        RunningLog(message = "Starting thread[{:}]".format(self.threadID), module = "DownloadPushThread", level=4)

        DownloadPush(self.target)
        
        RunningLog(message = "Stop thread[{:}]".format(self.threadID), module = "DownloadPushThread", level=4)

def StartDownloadPushThread(threadID, target):
    mthread = DownloadPushThread(threadID, target)
    mthread.start()
##    threadID = threadID + 1
    

def ShowThreadCount():
    print "test={:}".format(threading.active_count())


def GetThreadCount():
    result = threading.active_count()
    return result

def GetDownloadThreadCount(BasicThreadCount):
    result = threading.active_count() - BasicThreadCount
    return result
    
