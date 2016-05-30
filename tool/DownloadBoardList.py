# -*- coding: utf8 -*-
import __init__
from lib import *
from WebHandler import *
from config import *
import os




Result_fopw = None
Log_fopw    = None


tmpURLList = []

# Get UserAgentList_path from config
CurrentFolder           = os.path.dirname(os.path.abspath(__file__))
ParentFolderPath        = os.path.abspath(os.path.join(CurrentFolder, os.pardir))
UserAgentListFilePath   = ParentFolderPath + "\\" + UserAgentList_Path.replace('/','\\')


def StoreResult(ResultURL):
    # Write into Result file
    Result_fopw.write(ResultURL + '\r\n')

def exeLog(message, module, level=5):
    mes = MessageHandler.RunningLog(message,module, level=level)
    if mes != None:
        Log_fopw.write(mes)
        Log_fopw.write('\r\n')

def error(message, module):
    mes = MessageHandler.ErrorLog(message, module)
    Log_fopw.write(mes)
    Log_fopw.write('\r\n')

def GetAllBoardLink(target, UserAgentList):

    response = WebConnector(target, UserAgentList)
    hreflist = GetItemsFromResponse(response, Pattern_GetHref)

    if len(hreflist) > 0:
        
        for href in hreflist:

            # Make sure the href  is sub page
            # not home page or other extend link
            if (href.find('.') > 0) & (href.find('http:') < 0):

                tmpURL = TranslateIntoFullURL(href)

                if UpdateDownloadURLList(tmpURL) == True:
                    if href.find('index.html') > -1:
                        # Get url of board
                        exeLog("Got board link: {:}".format(tmpURL), "GetAllBoardLink", 2)
                        StoreResult(tmpURL)
                    elif href.find('/1.html') > -1:
                        exeLog("Ignore tree root: {:}".format(tmpURL), "GetAllBoardLink", 2)
                    else:
                        # Get url of sub list page
                        exeLog("Got list page link: {:}".format(tmpURL), "GetAllBoardLink", 3)

                        try:
                            GetAllBoardLink(tmpURL, UserAgentList)
                        except:
                            error("Restart download : {:}".format(tmpURL), "GetAllBoardLink")
                            GetAllBoardLink(tmpURL, UserAgentList)


def GetBoardName(URL):
    BoardName = URL.split('/')[4]
    return BoardName

def CheckIfNameInList(checkName, nameList):
    # Check if item is already in list
    result = False
    for name in nameList:
        if checkName == name:
            exeLog("URL is already in list", "CheckIfNameInList", 4)
            result = True
            return result
        else:
            exeLog("URL is not in list", "CheckIfNameInList", 4)
            result = False
            
    return result

def UpdateDownloadURLList(URL):
    # Add new item success: True
    # Add new item fail   : False
    result = False
    
    tmpURLName  = GetBoardName(URL)
    
    result      = CheckIfNameInList(tmpURLName, tmpURLList)
    
    if result == False:
        exeLog("Add new URL into tmpURLList", "UpdateDownloadURLList", 4)
        tmpURLList.append(tmpURLName)
        result = True
        
    return result
   

if __name__ == '__main__':
    
    Result_fopw = open(ResultFilePath, 'wb')
    Log_fopw    = open(LogFilePath, 'wb')

    
    exeLog("Get user-agent list", "Main", 2 )
    UserAgentList   = LoadUserAgentList(UserAgentListFilePath)
    
    exeLog("Start download url", "Main", 2 )
    exeLog("Start from : {:}".format(PttTreeStart), "Main", 2 )
    GetAllBoardLink(PttTreeStart, UserAgentList)

    Result_fopw.close()
    Log_fopw.close()

##    GetBoardName(PttTreeStart)
