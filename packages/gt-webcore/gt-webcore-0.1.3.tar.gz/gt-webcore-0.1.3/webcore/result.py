# coding:utf-8
from .constant import Error
from .exception import GtBaseError

class Result(object):    
    def __init__(self, code, msg='', data = None):
        self.code = code
        self.msg = msg
        self.data = data

    @classmethod
    def ok(cls):
        return Result(Error.OK, 'success')

    @classmethod
    def error(cls, base_error = None):
        if (base_error == None):
            return Result(Error.SERVER_ERROR, 'server error')
        else:
            return Result(base_error.code, base_error.msg)

    @classmethod
    def http_error(cls, msg = None):
        return Result(Error.HTTP_ERROR,  msg or 'http error')
    
    @classmethod
    def db_error(cls):
        return Result(Error.DB_ERROR, 'database error')

    @classmethod
    def author_error(cls):
        return Result(Error.AUTHOR_ERROR, "authorization error")

    @classmethod
    def json_error(cls):
        return Result(Error.JSON_ERROR, "JSON parse error")

    def set_data(self, data):
        self.data = data
        return self
    
    def set_page_data(self, page_data):
        self.data = page_data.items
        self.page = page_data.page
        self.size = page_data.per_page
        self.total = page_data.total
        return self

    def set_code(self, code):
        self.code = code
        return self

    def set_msg(self, msg):
        self.msg = msg
        return self
