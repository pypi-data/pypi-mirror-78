# coding:utf-8
from enum import Enum
import os

VERSION = '0.1.3'

class Error(Enum):
    UNKOWN                      = -1
    OK                          =  0
    SERVER_ERROR                =  1
    DB_ERROR                    =  2
    HTTP_ERROR                  =  3
    JSON_ERROR                  =  4
    AUTHEN_ERROR                =  5
    AUTHOR_ERROR                =  6
    PARAMS_ERROR                =  7
    OBJECT_NOT_EXSIT            =  8
    OBJECT_IS_EXSIT             =  9

