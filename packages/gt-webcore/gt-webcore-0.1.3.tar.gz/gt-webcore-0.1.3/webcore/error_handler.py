from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app as app
from json import JSONDecodeError
from .result import Result
from .constant import Error
from . import exception

def _handle_error(e):
    if isinstance(e, HTTPException):
        app.logger.error('Http Exception.', exc_info = True)
        
        if e.code == 400:
            return Result.http_error(e.data.get('message'))
            
        return Result.http_error(e.name)
    elif isinstance(e, SQLAlchemyError):
        app.logger.error('SqlAlchemy Exception.', exc_info = True)
        return Result.db_error()
    elif isinstance(e, JSONDecodeError):
        app.logger.error('JSON Exception.', exc_info = True)
        return Result.json_error()
    elif isinstance(e, exception.GtBaseError):
        # app.logger.error('Gt Base Error.', exc_info = True)
        return Result.error(e)
    elif isinstance(e, TypeError):
        app.logger.error('Type Error.', exc_info = True)
    elif isinstance(e, Exception):
        app.logger.error('Unkown Exception.', exc_info = True)

    return Result.error()

def init_error_handler(app):
    app.register_error_handler(Exception, _handle_error)
