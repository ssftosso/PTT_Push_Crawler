# -*- coding: utf8 -*-
import os

## Show log
    #  top: 0
    # down: 5 (default)
RunningLogLevel = 2

## Multi-Thread set
EnableMultiThread = False
MaxMultiThreadNum = 3

ThreadCountCheckDelay           = 1 # for waiting all thread finished
MaxMultiThreadNum_CheckDelay    = 1

## DelayTime
GetAndStorePushList_ErrorDelay = 2

#### Delay time config
ERROR_xpath_delay = 1

## URL config
RootURL = "https://www.ptt.cc"

##Database config
DB_DatabaseName = "STORE.db"

DB_TableName    = "PushList"

DBC_TypeName    = "type"
DBC_AccountName = "account"
DBC_PushContent = "content"
DBC_PostTitle   = "posttitle"
DBC_PostAccount = "postaccountname"
DBC_BoardName   = "board"
DBC_PushTime    = "pushtime"

#### File set
UserAgentList_Path              = 'item/UserAgentList.txt'



#### tool/DownloadBoardList.py

PttTreeStart    = "https://www.ptt.cc/bbs/1.html"
ResultFilePath  = "PTTURLList.txt"

LogFilePath = "Log.txt"
