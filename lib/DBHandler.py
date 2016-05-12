# -*- coding: utf8 -*-
import __init__ 
from config import *
from item import *
from MessageHandler import *

import sqlite3

## Database function
def DatabaseInitial():
    # Create New Database
    conn = GetDBconector()
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

    RunningLog("Database initial done", level=2)
    conn.close()

def GetDBconector():
    try:
        return sqlite3.connect(DB_DatabaseName)
    except:
        ErrorLog("DB connect fail", "GetDBconnector")
        return GetDBconnector()


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
        del cmd
        del push
        del DBconnector
        
    except:
        ErrorLog("DB insert error. Start reinserting.", "DBInsertPush")
        DBInsertPush(DBconnector, push)


def DBInsertPushList(DBconnector, PushList):
    try:
        for push in PushList:
            DBInsertPush(DBconnector, push)

        # release memory
        del PushList[:]; del PushList
    except:
        ErrorLog("Push list insert fail","DBInsertPushList")


def DBSelectAll():
    DBconnector = GetDBconector()
    cmd = DBconnector.cursor()
    CMD_SelectAll = "SELECT content FROM " + DB_TableName
    for row in cmd.execute(CMD_SelectAll):
        print row[0]

    DBconnector.close()
