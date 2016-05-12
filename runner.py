# -*- coding: utf8 -*-
from item import *
from lib import *
from MessageHandler import *
from config import *

##from ThreadHandler import *

import thread, threading



if __name__ == '__main__':
    DBHandler.DatabaseInitial()

    target = objects.Target("https://www.ptt.cc/bbs/StupidClown/index.html", "StupidClown")


    BasicThreadCount = ThreadHandler.GetThreadCount()
    threadCount = 0

    # Get user-agent list
    UserAgentList = WebHandler.LoadUserAgentList()

    # PreURL is for while loop checking
    PreURL = ''

    # Thread ID not used yet.
    threadID = 0

    if EnableMultiThread == True:
        # for multi-thread
        while PreURL is not None:
            # Get num of download threads
            # For limit max num of threads
            DownloadThreadCount = ThreadHandler.GetDownloadThreadCount(BasicThreadCount)

            while DownloadThreadCount >= MaxMultiThreadNum:
                logmessage = "[Thread Wait] Num of Thread={:}, Wait {:} seconds".format(DownloadThreadCount, MaxMultiThreadNum_CheckDelay)
                RunningLog(message=logmessage, level=0, module="MAIN")

                # Wait for empty thread
                ErrorHandler.Delay(MaxMultiThreadNum_CheckDelay)

                # If num of thread is bigger than MaxMultiThreadNum, then waiting for thread be free
                DownloadThreadCount = ThreadHandler.GetDownloadThreadCount(BasicThreadCount)
            
            # Creat and Start download push thread
            ThreadHandler.StartDownloadPushThread(threadID, target)
                
            # Get pre url
            PreURL = WebHandler.GetPrePageURL_fromTarget(target, UserAgentList)
                
            # Asign new url to target
            # Object:[target] will be reused in the while loop
            target.URL = PreURL


        while threadCount is not 0:
            # Get thread num of download threads            
            DownloadThreadCount = ThreadHandler.GetDownloadThreadCount(BasicThreadCount)
            RunningLog(message="[Not fished thread count=]={:}, plz wait".format(DownloadThreadCount), level=0, module="MAIN")

            # for waiting all thread finished
            ErrorHandler.Delay(ThreadCountCheckDelay)

        RunningLog("All threads are finished","MAIN")
        
    elif EnableMultiThread == False:
        while PreURL is not None:

            # Start download push
            WebHandler.DownloadPush(target)

            # Get pre url
            PreURL = WebHandler.GetPrePageURL_fromTarget(target, UserAgentList)
            
            # Asign new url to target
            # Object:[target] will be reused in the while loop
            target.URL = PreURL
            
    

