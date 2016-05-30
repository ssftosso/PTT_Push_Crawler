# -*- coding: utf8 -*-
import __init__ 
from config import *

from pattern import WebPattern
from WebPattern import *

from item import *
from DBHandler import *
from MessageHandler import *
from StringHandler import *
from ThreadHandler import *
from ErrorHandler import *

import random
import re
from lxml import html, etree
import requests
import time




# Get user-agent list from file in folder: item
# return list
def LoadUserAgentList(UserAgentList_filePath = UserAgentList_Path):
    # UserAgentList_Path is in config
    op = open(UserAgentList_filePath, 'r')

    UserAgentList = []
    for line in op:
        # except # line
        if line.find('#') != 0:
            line = line.replace('\n','')
            UserAgentList.append(line)
            
    op.close()
    RunningLog("user-agent list loaded", "LoadUserAgentList")
    return UserAgentList


def GetRandomUserAgent(UserAgentList):
## Since use same user-agent will be block by server.
## so we randomly get user-agent from user-agent list
    MaxNum = len(UserAgentList)
    RandomID = random.randint(0,MaxNum-1)

    UserAgent = UserAgentList[RandomID]
    if (UserAgent != '') & (UserAgent != None) & (UserAgent != '\n'):
        RunningLog("user-agent:{:}".format(UserAgent), "GetRandomUserAgent")
        
        return UserAgent
    else:
        ErrorLog("Get error value and reseting user-agent", "GetRandomUserAgent")
        return GetRandomUserAgent(UserAgentList)

    

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

    RunningLog("Set header", "WebConnector")


    Response = requests.get(URL, headers = Headers)
    hr = html.fromstring(GetContentWithCorrectEncode(Response))

    try:
    
##    try:
##        Response = requests.get(URL, headers = Headers)

        if Error != None:
            ErrorLog("Response","WebConnector")

        try:
            # check encode:
            # StringHandler.GetContentWithEncode
            htmlResponse = html.fromstring(GetContentWithCorrectEncode(Response))
##            htmlResponse = html.fromstring(Response.text)
            try:
                Response.connection.close()
            except:
                ErrorLog("Response close fail", "Response")

            if (htmlResponse != None) & (htmlResponse != ''):
                
                Error = None
                del Response
                return htmlResponse
            else:
                ErrorLog("Response is empty", "Response")
                return Reconnect(URL, UserAgentList, Error)
        except:
            ErrorLog("html.fromstring error", "html.fromstring")
            return Reconnect(URL, UserAgentList, Error)
    except:
        ErrorLog("Request fail", "requests.get")
        return Reconnect(URL, UserAgentList, Error)


def Reconnect(URL, UserAgentList, Error):
    ErrorLog("reconnecting")
    Error = objects.DelayError(Error)
    return WebConnector(URL,UserAgentList, Error)


def GetItemsFromResponse(Response, Pattern):
    try:
        RunningLog("get xpath from response", "GetItemsFromResponse")
        return Response.xpath(Pattern)
    except:
        ErrorLog("Restarting GetItemsFromResponse", "GetItemsFromResponse")
        Delay(ERROR_xpath_delay)
        return GetItemsFromResponse(Response, Pattern)


def TranslateIntoFullURL(relatedURLList):
    # Translate related URL into Full URL

    RunningLog("Translate related URL into full URL", "TranslateIntoFullURL")
    
    FullURLList = []
    try:
        ## Check shortURLList is list or string
        if isinstance(relatedURLList, list) == True:
            for relatedURL in relatedURLList:
                if relatedURL.find('http') == -1:
                    tmpFullURL = RootURL + relatedURL
                    FullURLList.append(tmpFullURL)
        elif isinstance(relatedURLList, str) == True:
            FullURLList = RootURL + relatedURLList
    except:
        ErrorLog("Translate from releated into full url", "TranslateIntoFullURL")

    return FullURLList



def GetPushList(Response , target):
    # Get push list from response
    RunningLog("Get push list from response", "GetPushList")
    
    PushList = []

    try:
        PostAccount     = GetItemsFromResponse(Response, Pattern_PostAccountInSubPage)[0]
        PostAccount     = PostAccount.split(' ')[0]        
    except:
        PostAccount     = "PostAccountError"

    
    try:
        PostTitle       = GetItemsFromResponse(Response, Pattern_TitleInSubPage)[0]
    except:
        PostTitle       = "TITLE ERROR"
        
    PushTypeList        = GetItemsFromResponse(Response, Pattern_PushType)
    PushAccountList     = GetItemsFromResponse(Response, Pattern_PushAccount)
    PushContentList     = GetItemsFromResponse(Response, Pattern_PushContent)
    PushTimeList        = GetItemsFromResponse(Response, Pattern_PushTime)

    PushSum = len(PushTimeList)

    try:
        for counter in range(0, PushSum,1):
            newPush = objects.Push()

            try:
                newPush.Title       = PostTitle
                newPush.PostAccount = PostAccount
                newPush.Type        = PushTypeList[counter]
                newPush.Account     = PushAccountList[counter]
                
                ## It will get string array for the response with href
                try:
                    tmpContent          = PushContentList[counter].xpath('.//text()')
                except:
                    ErrorLog("Get tempContent fail","GetPushList-tempContent")

                try:
                    newPush.Content     = ArrayInto1String(tmpContent)
##                    newPush.Content = temp
                except:
                    ErrorLog("Get content to push list fail","GetPushList-newPush.Content")
                
                newPush.Time        = PushTimeList[counter].replace('\n','')
                newPush.Board       = target.BoardName
                
                PushList.append(newPush)
                
            except:
                ErrorLog("Add new object into list","GetPushList-PushList.append")

            # release memory
            # del newPush

        
    except:
        ErrorLog("'for' loop for getting push list fail", "GetPushList")
        return GetPushList(Response , target)
    # release memory
    RunningLog("release list", "GetPushList")
##    del PushTypeList[:]
##    del PushAccountList[:]
##    del PushContentList[:]
##    del PushTimeList[:]    
    return PushList

def GetPrePageURL_fromTarget(target, UserAgentList):
    try:
        WebResponse = WebConnector(target.URL, UserAgentList)
        PreURL      = GetPrePageURL_fromResponse(WebResponse)
        return PreURL
    except:
        ErrorLog("Get pre url fail. Restart.","GetPrePageURL_fromTarget")
##        PreURL = None
        return GetPrePageURL_fromTarget(target, UserAgentList)
        
        
    

def GetPrePageURL_fromResponse(response):

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
        
        RunningLog("------ End of Page ------")
        print "------ End of Page ------"
        return None
    else:
        RunningLog("PreURL:{:}".format(PreURL), "GetPrePageURL_fromResponse")
        return PreURL


def GetAndStorePushList(response, UserAgentList, targetInfo):
    
##    # Get Subpage title list
##    SubPageTitleList = GetItemsFromResponse(Response, Pattern_SubPageTitle)
    
    # Get Subpage url list
    SubPageURLList_related = GetItemsFromResponse(response, Pattern_SubPageURL)

    # Set database connector
    DBconnector = GetDBconector()

    try:
        if len(SubPageURLList_related) > 0:
            SubPageURLList_full = TranslateIntoFullURL(SubPageURLList_related)

            try:
                for SubPageURL in SubPageURLList_full:
                    SubResponse = WebConnector(URL=SubPageURL, UserAgentList=UserAgentList)
                    
                    # Get Title
                    try:
                        PostTitle   = GetItemsFromResponse(SubResponse, Pattern_TitleInSubPage)[0]
                    except:
                        PostTitle   = "-- Title Error --"

                    try:
                        # Get Push LIST
                        PushList    = GetPushList(SubResponse, targetInfo)
                        RunningMessage = "[Downloaded][Pushes: {:<5}] ".format(str(len(PushList))) + PostTitle
                        RunningLog(RunningMessage, level=3)
##                        print "[Downloaded][Pushes: {:<5}] ".format(str(len(PushList))) + PostTitle

                        RunningLog("Storing into database")
                        DBInsertPushList(DBconnector, PushList)

                        # release list
                        del PushList
                    except:
                        ErrorLog("PushList fail", "GetAndStorePushList")
                        return GetAndStorePushList(response, UserAgentList, targetInfo)
                        

                # release memory
                del SubPageURLList_full[:]
            except:
                ErrorLog("'for' loop for SubPage", "GetAndStorePushList")
                
                return GetAndStorePushList(response, UserAgentList, targetInfo)

##            # Memory garbage
##            del SubPageURLList_full[:]

    except:
        ErrorLog("Restart DownloadPush", "GetAndStorePushList")
        return GetAndStorePushList(response, UserAgentList, targetInfo)

    # Memory garbage
    del SubPageURLList_related[:]
    DBconnector.close()



def DownloadPush(target):

    TargetURL = target.URL
    
    RunningLog("Target:{:}".format(TargetURL), level=0)
    
    # Get Header List
    UserAgentList = LoadUserAgentList()

    #Get response
    Response = WebConnector(URL=TargetURL, UserAgentList=UserAgentList)
    
    
    GetAndStorePushList(Response, UserAgentList, targetInfo=target)
    

