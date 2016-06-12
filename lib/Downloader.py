# -*- coding: utf8 -*-
import __init__ 
from config import *
from pattern import *
from item import *

from DBHandler import *
from MessageHandler import *
from StringHandler import *
from ThreadHandler import *
from ErrorHandler import *
from WebHandler import *

import datetime
import random
import signal
import os
from shutil import copyfile


def GetUrlInFile(filepath, Num):
    result = None
    if os.path.isfile(filepath):
        with open(filepath, 'r') as fop:
            # Get last line of file
            try:
                result = fop.readlines()[Num].replace('\n','')
            except Exception:
                result = None

    return result

def GetLastUrlInFile(filepath):
    result = GetUrlInFile(filepath, -1)
    return result

def GetSecondUrlInFile(filepath):
    result = GetUrlInFile(filepath, 1)
    return result

def CopyTmpFile(filePath):
    # This function is effect with runner in function -b:all
    # code: if re.search("\d{5}tmp", filename) is None:
    print filePath
    randomNum = random.randrange(1,10000)
    tmpFileName = filePath + ".{:0<5}tmp".format(randomNum)
    if os.path.isfile(filePath) is True:
        if os.path.isfile(tmpFileName) is not True:
            RunningLog("Create tmp file :{:}".format(tmpFileName),"CopyTmpFile",level=4)
            copyfile(filePath,tmpFileName)
            return tmpFileName
        else:
            CopyTmpFile(filePath)
    else:
        return None


def UpdateUrlList(TargetURL):
    
    target = objects.Target(TargetURL, GetBoardName(TargetURL))
    
    # Get user-agent list
    UserAgentList = LoadUserAgentList()

    # Get tmp file path
    TmpUrlListFilePath = URLListFileRootPath + "\\" + target.BoardName + ".txt"

    # Get last url that downloaded in the past
    LastUrlInHistory = GetLastUrlInFile(TmpUrlListFilePath)

    # Get second url that downloaded in the past
    SecondUrlInHistory = GetSecondUrlInFile(TmpUrlListFilePath)

    # Tmp data for checking list
    if TmpUrlListFilePath is not None:
        TmpCopyUrlListFilePath = CopyTmpFile(TmpUrlListFilePath)

    TCULF_OP = None
    if TmpCopyUrlListFilePath is not None:
        TCULF_OP = open(TmpCopyUrlListFilePath,'rb')
        
    with open(TmpUrlListFilePath, 'a') as TULF_OP:

            # Initial PreURL
        PreURL = target.URL
            
        while PreURL is not None:
                
            newURL = PreURL
            if TCULF_OP is not None:
                TCULF_OP.seek(0) # reset file point 
                if newURL in TCULF_OP.read():
                    RunningLog("URL {:} is already existed.".format(newURL),"",level=2)
                else:
                    RunningLog("URL {:} writing into file {:}".format(newURL, TmpUrlListFilePath),"",level=5)
                    TULF_OP.write(newURL + "\n")

                if (newURL in TCULF_OP.read()) & (newURL.find("index.html") == -1):
                    break
            else:
                RunningLog("URL {:} writing into file {:}".format(newURL, TmpUrlListFilePath),"",level=5)
                TULF_OP.write(newURL + "\n")
                
            # Get next page url
            PreURL = GetPrePageURL_fromTarget(target, UserAgentList)
            target.URL = PreURL
    
    if TCULF_OP is not None:
        TCULF_OP.close()
        os.remove(TmpCopyUrlListFilePath)
        

def DownloadBoardPushFromFile(FilePath):
    if os.path.isfile(FilePath) is True:
        rop = open(FilePath, 'r')
        RunningLog("ReadFile: {:}".format(FilePath),"DownloadBoardPushFromFile",level=3)
        for url in rop.readlines():
            url = url.replace('\n', '')
            DownloadSingleBoardPush(url)


def DownloadSingleBoardPush(TargetURL):
    #Set timer
    StartTimeFlag = datetime.datetime.now()
    
    target = objects.Target(TargetURL, GetBoardName(TargetURL))
    
    # Initial database
    DatabaseInitial(target.BoardName)
    
    BasicThreadCount = GetThreadCount()
    threadCount = 0

    # Get user-agent list
    UserAgentList = LoadUserAgentList()

    # Thread ID not used yet.
    threadID = 0

    # PreURL initial
    PreURL = target.URL

    if EnableMultiThread == True:
        # for multi-thread
        while PreURL is not None:
            # Get num of download threads
            # For limit max num of threads
            DownloadThreadCount = GetDownloadThreadCount(BasicThreadCount)

            while DownloadThreadCount >= MaxMultiThreadNum:
                logmessage = "[Thread Wait] Num of Thread={:}, Wait {:} seconds".format(DownloadThreadCount, MaxMultiThreadNum_CheckDelay)
                RunningLog(message=logmessage, level=0, module="DownloadSingleBoarderPush")

                # Wait for empty thread
                Delay(MaxMultiThreadNum_CheckDelay)

                # If num of thread is bigger than MaxMultiThreadNum, then waiting for thread be free
                DownloadThreadCount = GetDownloadThreadCount(BasicThreadCount)
            
            # Creat and Start download push thread
            StartDownloadPushThread(target, threadID)
                
            # Get pre url
            PreURL = GetPrePageURL_fromTarget(target, UserAgentList)
                
            # Asign new url to target
            # Object:[target] will be reused in the while loop
            target.URL = PreURL

        
        while DownloadThreadCount is not 0:
            # Get thread num of download threads            
            DownloadThreadCount = GetDownloadThreadCount(BasicThreadCount)
            RunningLog(message="[Not fished thread count=] {:}, plz wait".format(DownloadThreadCount), level=0, module="DownloadSingleBoarderPush")

            # for waiting all thread finished
            Delay(ThreadCountCheckDelay)

        RunningLog("All threads are finished","DownloadSingleBoarderPush")
        
    elif EnableMultiThread == False:
        while PreURL is not None:          
            # Start download push
            DownloadPush(target)
            
            # Get pre url
            PreURL = GetPrePageURL_fromTarget(target, UserAgentList)
            
            # Asign new url to target
            # Object:[target] will be reused in the while loop
            target.URL = PreURL
            PreURL = None

        
    EndTimeFlag = datetime.datetime.now()

    RunningLog(message="Download time={:}".format(EndTimeFlag-StartTimeFlag), level=0, module="DownloadSingleBoarderPush")



