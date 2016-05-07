# -*- coding: utf8 -*-
from lxml import html, etree
import requests
import time
import re
import os
import sqlite3
import random
import datetime
import gc

from config import *
from objects import *

'''
 Date : 2016/05/05
 Time : 1845
 Note :
         Function:
            > Add more memory release
            > Add more except

 Date : 2016/05/03
 Time : 1845
 Note :
         Function:
            > Add memory release
            > Add garbage collector
            > fix except return function


 Date : 2016/05/02
 Time : 2350
 Note :
         Function:
            > Add error exceptions

         Issue:
            > Get response from reconnection but still get error


 Date : 2016/05/01
 Time : 1700
 Note :
         Function:
            > Download push with random user-agent (DONE)
            > Store into DB (DONE)
            > Add memory release
            > Add garbage collector
'''
# enable auto collect the garbage
gc.enable



## Database function
def DatabaseInitial():
    # Create New Database
    conn = sqlite3.connect(DB_DatabaseName)
    cmd = conn.cursor()

    CMD_CreateDB = "CREATE TABLE IF NOT EXISTS " + DB_TableName
    CMD_CreateDB = CMD_CreateDB + " (id INTEGER PRIMARY KEY AUTOINCREMENT,"
    CMD_CreateDB = CMD_CreateDB + DBC_BoardName     + " text" + ","
    CMD_CreateDB = CMD_CreateDB + DBC_PostTitle     + " text" + ","
    CMD_CreateDB = CMD_CreateDB + DBC_TypeName      + " text" + ","
    CMD_CreateDB = CMD_CreateDB + DBC_AccountName   + " text" + ","
    CMD_CreateDB = CMD_CreateDB + DBC_PushTime      + " text" + ","
    CMD_CreateDB = CMD_CreateDB + DBC_PushContent   + " text" +  ")"

    cmd.execute(CMD_CreateDB)

    conn.commit()
    
    del cmd
    del CMD_CreateDB
    
    return conn


def DBInsertPush(DBconnector, push):

    try:
        cmd = DBconnector.cursor()
        CMD_InsertDB = ''
        CMD_InsertDB = "INSERT INTO " + DB_TableName
        CMD_InsertDB = CMD_InsertDB + "("
        CMD_InsertDB = CMD_InsertDB + DBC_BoardName     + "," 
        CMD_InsertDB = CMD_InsertDB + DBC_PostTitle     + "," 
        CMD_InsertDB = CMD_InsertDB + DBC_TypeName      + "," 
        CMD_InsertDB = CMD_InsertDB + DBC_AccountName   + ","
        CMD_InsertDB = CMD_InsertDB + DBC_PushTime      + "," 
        CMD_InsertDB = CMD_InsertDB + DBC_PushContent   + ") " 
        CMD_InsertDB = CMD_InsertDB + "VALUES"
        CMD_InsertDB = CMD_InsertDB + " (?,?,?,?,?,?)"

        InsertValues = (push.Board,\
                        push.Title,\
                        push.Type,\
                        push.Account,\
                        push.Time,\
                        push.Content)

        cmd.execute(CMD_InsertDB, InsertValues)

        DBconnector.commit()
        
        # release memory
        del push
        del DBconnector
    except:
        print "[ERROR] DB insert error. Start reinserting."
        DBInsertPush(DBconnector, push)


def DBInsertPushList(DBconnector, PushList):
    for push in PushList:
        DBInsertPush(DBconnector, push)

    # release memory
    del PushList[:]; del PushList
        

def DBSelectAll(DBconnector):
    cmd = DBconnector.cursor()
    CMD_SelectAll = "SELECT content FROM " + DB_TableName
    for row in cmd.execute(CMD_SelectAll):
        print row[0]


## Load headers from header list file
## return headerlist
def LoadUserAgentList():
    op = open(UserAgentList_Path, 'r')

    UserAgentList = []
    for line in op:
        if line.find('#') != 0:
            line = line.replace('\n','')
            UserAgentList.append(line)
            
    op.close()
    
    return UserAgentList


def GetRandomUserAgent(UserAgentList):
## Since use same user-agent will be block by server.
## so we randomly get user-agent from user-agent list
    MaxNum = len(UserAgentList)
    RandomID = random.randint(0,MaxNum-1)

    UserAgent = UserAgentList[RandomID]
    if (UserAgent != '') & (UserAgent != None) & (UserAgent != '\n'):
        del UserAgentList
        del RandomID
        return UserAgent
    else:
        print "[ERROR][user-agent]: Get error value and reseting user-agent"
        return GetRandomUserAgent(UserAgentList)

def Reconnect(URL, UserAgentList, Error):
    Error = DelayError(Error)
    return WebConnector(URL,UserAgentList, Error)

##def ReHtmlFormat(Response):
##    try:
##        htmlResponse = html.fromstring(Response.content)
##        return htmlResponse
##    except:
##        print "[ERROR][html.fromstring] Reformating"
##        return ReHtmlFormat(Response)


def WebConnector(URL, UserAgentList, Error = None ):
    Response        = None
    session         = None
    htmlResponse    = None

    UserAgent = GetRandomUserAgent(UserAgentList)
    
    
    # Set header: user-agent
    if Error is None:
        Headers = {
            'user-agent':UserAgent,
            'keep-alive':'False',
            'Connection':'close'
            }
    else:
        print "[user-agent]:" + UserAgent
        Headers = {
            'user-agent':UserAgent,
            }

    try:
        Response = requests.get(URL, headers = Headers)

        # for debug
        if Error != None:
            print Response.text

        try:
            htmlResponse = html.fromstring(Response.text)
            
            try:
                Response.connection.close()
            except:
                print "[Error][Response] Response close fail"

            if (htmlResponse != None) & (htmlResponse != ''):
                
                Error = None
                del Response
                return htmlResponse
            else:
                print "[ERROR] Response is empty"
                return Reconnect(URL, UserAgentList, Error)
        except:
            print "[ERROR] html.fromstring error"
            return Reconnect(URL, UserAgentList, Error)
    except:
        print "[ERROR] Request fail"
        return Reconnect(URL, UserAgentList, Error)

def GetItemsFromResponse(Response, Pattern):
    try:    
        return Response.xpath(Pattern)
    except:
        print "[ERROR][xpath] Restarting GetItemsFromResponse"
        Delay(ERROR_xpath_delay)
        return GetItemsFromResponse(Response, Pattern)

def TranslateIntoFullURL(shortURLList):
    # Translate URL into Full URL
    
    FullURLList = []
    ## Check shortURLList is list or string
    if isinstance(shortURLList, list) == True:
        for shortURL in shortURLList:
            if shortURL.find('http') == -1:
                tmpFullURL = RootURL + shortURL
                FullURLList.append(tmpFullURL)
    elif isinstance(shortURLList, str) == True:
        FullURLList = RootURL + shortURLList

    # release memory
    del shortURLList
    
    return FullURLList

def ArrayInto1String(array):
    result = ''
    for item in array:
        result = result + item

    del array[:]
    
    return result

def GetPushList(Response , target):
    PushList = []

    try:
        PostTitle       = GetItemsFromResponse(Response, Pattern_TitleInSubPage)[0]
    except:
        PostTitle       = "TITLE ERROR"
        
    PushTypeList        = GetItemsFromResponse(Response, Pattern_PushType)
    PushAccountList     = GetItemsFromResponse(Response, Pattern_PushAccount)
    PushContentList     = GetItemsFromResponse(Response, Pattern_PushContent)
    PushTimeList        = GetItemsFromResponse(Response, Pattern_PushTime)

    PushSum = len(PushTimeList)
    
    for counter in range(0, PushSum,1):
        newPush = Push()
        newPush.Title       = PostTitle
        newPush.Type        = PushTypeList[counter]
        newPush.Account     = PushAccountList[counter]
        
        ## It will get string array for the response with href        
        tmpContent          = PushContentList[counter].xpath('.//text()')        
        newPush.Content     = ArrayInto1String(tmpContent)
        
        newPush.Time        = PushTimeList[counter].replace('\n','')
        newPush.Board       = target.BoardName
        
        PushList.append(newPush)

        # release memory
        del newPush

    # release memory
    del PostTitle
    del PushTypeList[:]
    del PushAccountList[:]
    del PushContentList[:]
    del PushTimeList[:]
    
    return PushList

def GetPrePageURL(response):

    PreURL = ''
    
    tmp_PreURLs     = GetItemsFromResponse(response, Pattern_PrePageURL)
    tmp_PreNames    = GetItemsFromResponse(response, Pattern_PrePageName)

    FindPreURL = False

    for count in range(0, len(tmp_PreNames), 1):
        if tmp_PreNames[count].find(u'上頁') != -1:
            FindPreURL = True
            PreURL = TranslateIntoFullURL(tmp_PreURLs[count])

    # release memory
    del tmp_PreURLs
    del tmp_PreNames
    
    if FindPreURL == False:
        print "------ End of Page ------"
        return None
    else:
        return PreURL

def DownloadPush(target, DBconnector):

    TargetURL = target.URL
    print "[ Target ]: " + TargetURL
    
    # Get Header List
    UserAgentList = LoadUserAgentList()

    #Get response
    Response = WebConnector(URL=TargetURL, UserAgentList=UserAgentList)
    
    #Get Subpage title
    SubPageTitleList = GetItemsFromResponse(Response, Pattern_SubPageTitle)
    
    #Get Subpage url
    short_SubPageURLList = GetItemsFromResponse(Response, Pattern_SubPageURL)

    try:
        if len(short_SubPageURLList) > 0:
            SubPageURLList = TranslateIntoFullURL(short_SubPageURLList)


            for SubPageURL in SubPageURLList:
                SubResponse = WebConnector(URL=SubPageURL, UserAgentList=UserAgentList)
                # Get Title
                try:
                    PostTitle   = GetItemsFromResponse(SubResponse, Pattern_TitleInSubPage)[0]
                except:
                    PostTitle   = "-- Title Error --"
                
                # Get Push LIST
                PushList    = GetPushList(SubResponse, target)

                if Show_DetailLog is True:
                    print "[Downloaded][Pushes: {:<5}] ".format(str(len(PushList))) + PostTitle

                DBInsertPushList(DBconnector, PushList)            

                # release memory
                del SubResponse
                del PushList[:]

            # release memory
            del SubPageURLList[:]

        PreURL = GetPrePageURL(Response)

        # Memory garbage
        del Response
        del SubPageTitleList[:]
        del short_SubPageURLList[:]
        gc.collect()

        if PreURL != None:
            target.URL = PreURL
            DownloadPush(target, DBconnector)
        else:
            del DBconnector
            del target
                

    except:
        print "[ERROR][DownloadPush] Restart DownloadPush"
        DownloadPush(target, DBconnector)
    
    
    
if __name__ == '__main__':
    print "------ START ------"
    target = Target("https://www.ptt.cc/bbs/StupidClown/index.html", "StupidClown")
##    target = Target("https://www.ptt.cc/bbs/StupidClown/index10.html", "StupidClown")

    # DB initial
    DBconnector = DatabaseInitial()

##    # Load user-agent list
##    UserAgentList = LoadUserAgentList()
    
##    DBSelectAll(DBconnector)
    
    DownloadPush(target, DBconnector )

    DBconnector.close()
    
