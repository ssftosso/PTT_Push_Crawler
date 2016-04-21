# -*- coding: utf8 -*-
import urllib2
from lxml import html
import requests
import time
import re
import os
import sqlite3
import random
import datetime


'''
 Date : 2016/04/20
 Time : 0150
 Note :
         Function:
             RandomDelayTime
             DBInsertPushList
             DBSelectAll
         
         note:
             Work well so far

'''

# DB Database Name
DB_DatabaseName = "Datas.db"
    
# DB Table Name
DB_TableName = "PushList"
    
# DB Column Name
DBC_typeName = 'type'
DBC_nameName = 'name'
DBC_responseName = 'response'
DBC_timeName = 'time'
DBC_titleName = 'title'


class DelayTimeSet:
##    # DelayTime from page to page
##    DelayTimeP2P = 2
##
##    # DelayTime from subpage to subpage
##    DelayTimeSP2SP = 0.5
##
##    # DelayTime for Error restart
##    DelayTimeError = 5
    P2P = 0
    SP2SP = 0
    Error = 0

##    def __init__(self,P2P ,SP2SP, Error):
##        self.P2P = P2P
##        self.SP2SP = SP2SP
##        self.Error = Error
    
class PushResponse:
    type = ''
    name = ''
    response = ''
    time = ''
    title = ''
    
    def __init__(self,type,name,response, time, title):
        self.type = type
        self.name = name
        self.response = response
        self.time = time.replace('\n', '')
        self.title = title

    def show(self):
        print "[" + self.type + "] [" + self.time + "] [" + self.name + "] " + self.response

def FormatWebResponse(response):
    result = html.fromstring(response.read())
    return result

def GetWebResponse(url):
    response = urllib2.urlopen(url)
    return response

def GetWebResponseWithFormat(url):
    response = GetWebResponse(url)
    result = FormatWebResponse(response)
    return result

def GetPreviousPageURL(response):
    pattern_URL = '//a[@class="btn wide"]/@href'
    pattern_name = '//a[@class="btn wide"]/text()'

    ResultURLs = response.xpath(pattern_URL)
    ResultNames = response.xpath(pattern_name)

    PreviousPageItem = ResultNames[1]
    
    ResultURL = ''
    if PreviousPageItem.find(u'上頁') != -1:
        ResultURL = ResultURLs[1]
    else:
        ResultURL = 'END'
        
    return ResultURL

def GetSubPageURLs(response):
    pattern = '//div[@class="title"]/a/@href'
    return response.xpath(pattern)

def GetSubPageTitles(response):
    pattern = '//div[@class="title"]/a/text()'
    return response.xpath(pattern)


def GetTitleInSubPage(response):
    pattern = '//*[@id="main-content"]/div[3]/span[2]/text()'

    #Attation: [0]
    #withou this will cause chinese word cannot be translate from unicode to utf8
    try:
        title = response.xpath(pattern)[0]
    except:
        title = "Title ERROR"
    return title

def GetSubPageName(url):
    return url.split("/")[-1]

def GetGoodCount(response):
    pattern = '//*[@id="main-container"]/div/div/div/span/text()'
    return response.xpath(pattern)

def GetPushList(response, PageTitle):
    pattern_type = '//*[@id="main-content"]/div[@class="push"]/span[1]/text()'
    pattern_name = '//*[@id="main-content"]/div[@class="push"]/span[2]/text()'
    pattern_response = '//*[@id="main-content"]/div[@class="push"]/span[3]/text()'
    pattern_time = '//*[@id="main-content"]/div[@class="push"]/span[4]/text()'
    typeResponse = response.xpath(pattern_type)
    nameResponse = response.xpath(pattern_name)
    responseResponse = response.xpath(pattern_response)
    timeResponse = response.xpath(pattern_time)

    # All push in this response
    ResultList = []
    
    CountEnd = len(nameResponse)
    for count in range(0,CountEnd):
        tmpPush = PushResponse(typeResponse[count], nameResponse[count], responseResponse[count], timeResponse[count], PageTitle)
        ResultList.append(tmpPush)
    
    return ResultList


def GetFullURL(subURL ,urlroot):
    result = ""
    if subURL.find("http") == -1:
        # it's not a full url
        result = urlroot + subURL
    else:
        result = subURL
    return result

def ShowPushList(PushList):
    print "ShowPushList"
    '''
    type = ''
    name = ''
    response = ''
    time = ''
    title = ''
    '''
    for push in PushList:
        type = push.type
        title = push.title
        name = push.name
        time = push.time
        response = push.response

        message = "[" + title + "]" + "[" + type + "]" + "[" + time + "]" + "[" + name + "]" + " " + response
        print message

def DownloadAllPush(response, rooturl, DelayTime, DBconnector, SysLogOP):

    SumPagePushCount = 0 
    #Get sub page title
    for subURL in GetSubPageURLs(response):
        # Delay from subpage to subpage
        time.sleep(RandomDelayTime(DelayTime.SP2SP))
        
        FullSubURL = GetFullURL(subURL, rooturl)
        subResponse = GetWebResponseWithFormat(FullSubURL)

        # Get title of page
        SubTitle = GetTitleInSubPage(subResponse)
        SubPushList = GetPushList(subResponse, SubTitle)

        # Count pushes
        SumPagePushCount = SumPagePushCount + len(SubPushList)
        
        # Insert into DB
        DBInsertPushList(DBconnector, SubPushList)

        
    sysMessage =  "[SubPushCount]: " + str(SumPagePushCount)
    ShowMessage(SysLogOP, sysMessage)

    # Delay from page to page
    time.sleep(RandomDelayTime(DelayTime.P2P))

    #Go to previous page
    SubPreviousURL = GetPreviousPageURL(response)
    if SubPreviousURL != "END":
        PreviousPageFullURL = rooturl + SubPreviousURL
        sysMessage = "[GoTo]: "+  PreviousPageFullURL
        ShowMessage(SysLogOP, sysMessage)
        
        PreviousResponse = GetWebResponseWithFormat(PreviousPageFullURL)
        try:
            DownloadAllPush(PreviousResponse, rooturl, DelayTime, DBconnector, SysLogOP)
        except:
            ShowMessage(SysLogOP, "[ERROR]: Delay 5 seconds...")
            time.sleep(DelayTime.Error)

            ShowMessage(SysLogOP, "Restart again")
            DownloadAllPush(PreviousResponse, rooturl, DelayTime, DBconnector, SysLogOP)
    else:
        ShowMessage(SysLogOP, "END")



def DatabaseInitial():
    # Create New Database
    conn = sqlite3.connect(DB_DatabaseName)
    cmd = conn.cursor()

    CMD_CreateDB = "CREATE TABLE IF NOT EXISTS " + DB_TableName
    CMD_CreateDB = CMD_CreateDB + " (id INTEGER PRIMARY KEY AUTOINCREMENT,"
    CMD_CreateDB = CMD_CreateDB + DBC_titleName + " text" + ","
    CMD_CreateDB = CMD_CreateDB + DBC_typeName + " text" + ","
    CMD_CreateDB = CMD_CreateDB + DBC_nameName + " text" + ","
    CMD_CreateDB = CMD_CreateDB + DBC_timeName + " text" + ","
    CMD_CreateDB = CMD_CreateDB + DBC_responseName + " text" +  ")"

    cmd.execute(CMD_CreateDB)

    conn.commit()

    return conn
    
def DBInsertPushList(DBconnector, PushList):
#DBC_titleName = 'title'
#DBC_typeName = 'type'
#DBC_nameName = 'name'
#DBC_responseName = 'response'
#DBC_timeName = 'time'
    cmd = DBconnector.cursor()
    for push in PushList:
        CMD_InsertDB = ''
        CMD_InsertDB = "INSERT INTO " + DB_TableName
        CMD_InsertDB = CMD_InsertDB + "("
        CMD_InsertDB = CMD_InsertDB + DBC_titleName + "," 
        CMD_InsertDB = CMD_InsertDB + DBC_typeName + "," 
        CMD_InsertDB = CMD_InsertDB + DBC_nameName + "," 
        CMD_InsertDB = CMD_InsertDB + DBC_timeName + "," 
        CMD_InsertDB = CMD_InsertDB + DBC_responseName + ") " 
        CMD_InsertDB = CMD_InsertDB + "VALUES"
        CMD_InsertDB = CMD_InsertDB + " (?,?,?,?,?)"

        Values = (push.title , push.type, push.name, push.time, push.response)
        cmd.execute(CMD_InsertDB, Values)

    DBconnector.commit()

def DBSelectAll(DBconnector):
    cmd = DBconnector.cursor()
    CMD_SelectAll = "SELECT response FROM " + DB_TableName
    for row in cmd.execute(CMD_SelectAll):
        print row[0]

def RandomDelayTime(MaxTime):
    return random.random()*MaxTime

def ShowMessage(SysLogOP, message):
    print message
    SysLogOP.write(message)


if __name__ == '__main__':
    TargetURL = "https://www.ptt.cc/bbs/StupidClown/index.html"
    URLRootPath = "https://www.ptt.cc"
    FileRootPath = ""

    LogFileCreateTime = str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"))
    LogFileBasicName = 'SysLog_'
    LogFileName = LogFileBasicName + LogFileCreateTime + ".txt"
    
    

    # Syslog operater
    print "[Create Log]: " + LogFileName
    SysLogOP = open(LogFileName, 'wb')

    DelayTime = DelayTimeSet()
    # DelayTime from page to page
    DelayTime.P2P = 2

    # DelayTime from subpage to subpage
    DelayTime.SP2SP = 0.5

    # DelayTime for Error restart
    DelayTime.Error = 5

    # Database initial
    DBconnector = DatabaseInitial()

    # Get first url response
    Response = GetWebResponseWithFormat(TargetURL)

    
    print TargetURL
    try:
        DownloadAllPush(Response, URLRootPath, DelayTime, DBconnector, SysLogOP)
    except:
        print "Download ERROR"

    #DBSelectAll(DBconnector)
    
    DBconnector.close()

    SysLogOP.close()
    
