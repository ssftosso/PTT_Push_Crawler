# PTT Push Crawler
use Python 2.7(test)
## Introduction

This crawler can download all push of PTT posts. 

這隻爬蟲可以下載PTT文章的推文。


## Command
使用基本順序：
        ``` [-u] => [-p all] => [-b all] ```

註：目前尚無法得知全部下載所需時間，可能需要數天。

```
runner [-u] [-d] [-s|-m|-a] [-b URL]

-u, --update-board-list : 更新所有ptt版的首頁清單(index.html)
-p, --update-post-list  : 更新ptt版內所有分頁清單，將儲存於/urllist內，
                          此外，可以帶入"all"，此功能需要讀取-u所產生的
                          PTTURLList.txt。
-b, --boardURL          : 指定ptt URL，並下載該URL下所有推文，或是使用
                          "all" 讀取/urllist內所有url檔案，並執行下載。
Example:
    runner -p https://www.ptt.cc/bbs/Announce/index.html
    runner -p all
    runner -b https://www.ptt.cc/bbs/Announce/index.html
    runner -b all
```

## File tree
```
Crawler ┬─ runner.py                    : main function
        ├─ config.py                    : global setting
        ├─ __init__.py
        ├─ PTTURLList.txt               : all board url from too/DownloadBoardList.py                  
        ├─ lib ┬─ __init__.py  
        │      ├─ DBHandler.py          : function relate to database
        │      ├─ MessageHandler.py     : show running log, errorlog ... etc
        │      ├─ ErrorHandler.py       : Error delay
        │      ├─ StringHandler.py      : function relate to string
        │      ├─ ThreadHandler.py      : function relate to thread but it has some issue.
        │      └─ WebHandler.py         : function relate to web 
        ├─ ResultData                   : result in sqlite
        ├─ urllist                      : url under board
        ├─ pattern ┬─ __init__.py  
        │          └─ WebPattern.py     : pattern for xpath
        ├─ tool ┬─ __init__.py  
        │       ├─ DownloadBoardList.py : download index.html of all board
        └─ item ┬─ __init__.py   
                ├─ objects.py           : all object in used
                └─ UserAgentList.txt    : browser user-agent list
```

## Database schema
Database platform: sqlite

note: useful sqlite browser tool http://sqlitebrowser.org/

```
STORE.db ─ PushList ┬─ type             : push type. Include 推、噓...
                    ├─ account          : push account
                    ├─ content          : push content
                    ├─ posttitle        : post title
                    ├─ postaccountname  : post account
                    ├─ board            : board name. EX: 笨板(StupidClown)
                    └─ pushtime         : push time
```



