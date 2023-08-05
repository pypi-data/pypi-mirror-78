# -*- coding: utf-8 -
from flask import current_app as app
import functools

def auto_commit(auto = True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if auto:
                try:
                    app.db.session.commit()
                except Exception as error:
                    app.db.session.rollback()
                    raise error
                
            return result
        return wrapper
    return decorator

