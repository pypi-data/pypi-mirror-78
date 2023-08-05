# coding:utf-8
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.util._collections import AbstractKeyedTuple
from flask.json import JSONEncoder 
from flask_sqlalchemy.model import Model
from .result import Result
from .result import Error
import datetime

class ApiEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Model):
            return self.default({i.name: getattr(obj, i.name) for i in obj.__table__.columns})
        elif isinstance(obj, AbstractKeyedTuple):
            return self.default(obj._asdict())
        elif isinstance(obj, Result):
            return self.default(obj.__dict__)
        elif isinstance(obj, Error):
            return self.default(obj.value)
        elif isinstance(obj, list):
            obj_list = []

            for o in obj:
                obj_list.append(self.default(o))
            return obj_list
        elif isinstance(obj, dict):
            for k in obj:
                try:
                    obj[k] = self.default(obj[k])
                except TypeError:
                    obj[k] = None
            return obj
        elif isinstance(obj,datetime.datetime):
            return str(obj)
        else:
            return obj
