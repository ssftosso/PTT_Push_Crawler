# -*- coding: utf8 -*-
from item import *
from lib import *
from tool import *
from config import *

import sys,getopt
import re

def help_info():
    print '''
runner [-u] [-d] [-s|-m|-a] [-b URL]

-u, --update-board-list : Update all board url list
-p, --update-post-list  : Update URL list file which list all post URL
                          under each board in /data. Enter URL of board
                          or use "all" to update from PTTURLList.txt.
-b, --boardURL          : Select board you want to download and use ','
                          as multi url split or use "all" to download
                          all push of PTT.
Example:
    runner -p https://www.ptt.cc/bbs/Announce/index.html
    runner -p all
    runner -b https://www.ptt.cc/bbs/Announce/index.html
    runner -b all

'''

def GetUrlList(URLarray):
    result = URLarray.split(',')
    return result
    
if __name__ == '__main__':
    cDownload   = False
    cBoardURL   = None
    cAll        = False
    cUpdateBL   = False #update-board-list

    try:
        opts, args = getopt.getopt(sys.argv[1:], "dahup:b:", ["help", \
                                                            "update-board-list", \
                                                            "update-post-list=", \
                                                            "download", \
                                                            "all" ,\
                                                            "boardURL="])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                help_info()

            if opt in ("-u", "--update-board-list"):
                cUpdateBL = True
                MessageHandler.RunningLog("Updating board list...","MAIN", level=1)
                Downloader.DownloadBoardList()
                MessageHandler.RunningLog("Board list updated.","MAIN", level=1)

            elif opt in ("-p", "--update-post-list"):
                cPostURL = arg
                if cPostURL != "all":
                    for url in GetUrlList(cPostURL):
                        Downloader.UpdateUrlList(url)
                else:
                    print ResultFilePath
                    top = open(ResultFilePath,'r')
                    for url in top.readlines():
                        url = url.replace('\n','')
                        Downloader.UpdateUrlList(url)

            elif opt in ("-b", "--boardURL="):
                cBoardURL = arg
                if cBoardURL != 'all':
                    for url in GetUrlList(cBoardURL):
                        target = objects.Target(url, WebHandler.GetBoardName(url))
                        Downloader.DownloadSingleBoardPush(url)
                        MessageHandler.RunningLog("Download Finished: {:}".format(target.BoardName),"MAIN", level=1)
                elif cBoardURL == 'all':
                    PostUrlList = os.listdir(URLListFileRootPath)
                    for filename in PostUrlList:
                        if re.search("\d{5}tmp", filename) is None:
                            # Except tmp file in Downloader.CopyTmpFile
                            tmpfilepath = URLListFileRootPath + "\\" + filename
                            Downloader.DownloadBoardPushFromFile(tmpfilepath)

##            elif opt in ("-a", "--all"):
##                cAll = True
##                listop = open(ResultFilePath, 'r')
##                for url in listop:
##                    url = url.replace('\n','')
##                    Downloader.DownloadSingleBoardPush(url)

                listop.close()
        if len(opts) == 0:
            help_info()
        print opts
        MessageHandler.RunningLog("main function done","MAIN", level=1)
    except:
        help_info()


##DBHandler.DBSelectAll()


