# PTT Push Crawler
## Introduction

This crawler can download all push of PTT posts. I've successly download all push of board "StupidClown" and the next goal is download all PTT push. 

這隻爬蟲可以下載PTT文章的所有推文。 目前已經可以成功下載笨板的所有推文，下一個目標，是要下載所有的PTT推文。


### File tree
```
Crawler ┬─ runner.py                    : main function
        ├─ config.py                    : global setting
        ├─ __init__.py                  
        ├─ lib ┬─ __init__.py  
        │      ├─ DBHandler.py          : function relate to database
        │      ├─ MessageHandler.py     : show running log, errorlog ... etc
        │      ├─ ErrorHandler.py       : Error delay
        │      ├─ StringHandler.py      : function relate to string
        │      ├─ ThreadHandler.py      : function relate to thread but it has some issue.
        │      └─ WebHandler.py         : function relate to web 
        └─ item ┬─ __init__.py   
                ├─ objects.py           : all object in used
                └─ UserAgentList.txt    : browser user-agent list
```

### Database schema
```
STORE.db ─ PushList ┬─ type             : push type. Include 推、噓...
                    ├─ account          : push account
                    ├─ content          : push content
                    ├─ posttitle        : post title
                    ├─ postaccountname  : post account
                    ├─ board            : board name. EX: 笨板(StupidClown)
                    └─ pushtime         : push time
```



