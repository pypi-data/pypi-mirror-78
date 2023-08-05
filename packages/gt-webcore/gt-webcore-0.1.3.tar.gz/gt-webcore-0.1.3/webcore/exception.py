# coding:utf-8
from .constant import Error

class GtBaseError(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

class LoginError(GtBaseError):
    def __init__(self, msg = None):
        self.code = Error.AUTHEN_ERROR
        self.msg = msg or "User login failed"

class NotLoginError(GtBaseError):
    def __init__(self, msg = None):
        self.code = Error.AUTHEN_ERROR
        self.msg = msg or "User not login"

class ParamsError(GtBaseError):
    def __init__(self, msg = None):
        self.code = Error.PARAMS_ERROR
        self.msg = msg or "Parameters Error"

class ObjectNotExistError(GtBaseError):
    def __init__(self, msg = None):
        self.code = Error.OBJECT_NOT_EXSIT
        self.msg = msg or "Object Not Exist"

class ObjectIsExistError(GtBaseError):
    def __init__(self, msg = None):
        self.code = Error.OBJECT_IS_EXSIT
        self.msg = msg or "Object Is Exist"

class UserCanNotBeUsedError(GtBaseError):
    def __init__(self, msg = None):
        self.code = Error.AUTHOR_ERROR
        self.msg = msg or "User can not be used"

class TokenExpiredError(GtBaseError):
    def __init__(self, msg = None):
        self.code = Error.AUTHOR_ERROR
        self.msg = msg or "Token is expired"

class TokenParseError(GtBaseError):
    def __init__(self, msg = None):
        self.code = Error.AUTHOR_ERROR
        self.msg = msg or "Token can not be parsed"