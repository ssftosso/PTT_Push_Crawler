# -*- coding: utf8 -*-
import __init__ 
from config import *
from item import *
from MessageHandler import *


# combine array into one string
def ArrayInto1String(array):
    result = ''
    try:
        for item in array:
            result = result + item
    except:
        ErrorLog("Combine into one string fail","ArrayInto1String")

    return result


# set response.encoding into correcot encode
def ConfirmEncode(Response):
    RunningLog("Check Encode", "StringHandle.ConfirmEncode")
    if Response.encoding == 'utf-8':
        RunningLog("Encode: {:}".format(Response.encoding), "StringHandle.ConfirmEncode")
        return Response
    elif Response.encoding == 'ISO-8859-1':
        RunningLog("Encode: {:}".format(Response.encoding), "StringHandle.ConfirmEncode")
        Response.encoding = 'big5'
        return Response
    elif Response.encoding == 'big5':
        RunningLog("Encode: {:}".format(Response.encoding), "StringHandle.ConfirmEncode")
        Response.encoding = 'big5'
        return Response
    else:
        ErrorLog("Cannot recognize encode: {:}".format(Response.encoding), "StringHandle.ConfirmEncode")
        return Response

# set response.text into correct encode
def GetContentWithCorrectEncode(Response):
    Result = ''

    Response = ConfirmEncode(Response)
    
    if (Response.encoding == 'big5') | (Response.encoding == 'big-5') :
        RunningLog("set text encode into: {:}".format(Response.encoding), "StringHandle.GetContentWithCorrectEncode")
        Result = Response.text.encode('big5','ignore')
        return Result
    else:
        RunningLog(" The encode is not change : {:}".format(Response.encoding), "StringHandle.GetContentWithCorrectEncode")
        Result = Response.text
        return Result
        
