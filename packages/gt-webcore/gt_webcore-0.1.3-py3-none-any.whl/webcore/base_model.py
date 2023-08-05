# -*- coding: utf-8 -
from . import app
from sqlalchemy import Column, text, func, Index
from sqlalchemy import distinct
from sqlalchemy import desc
from sqlalchemy import update
from sqlalchemy.orm import aliased
from dotdict import DotDict

db = app.db

''' 数据表模型的基类'''
class BaseModel(db.Model):
    __abstract__ = True
    __table_args__ = {'mysql_engine': 'InnoDB'}

    def add(self, flush = True):
        db.session.add(self)
        if flush:
            db.session.flush()
        return self.id

    def remove(self):
        result = db.session.delete(self)
        return result

    def save(self, flush = False):
        result = (self.query.filter_by(id = self.id).update(self.to_dict()))

        if flush:
            db.session.flush()

        return result

    @classmethod
    def update(cls,sid,**row):
        return cls.query.filter_by(id=sid).update(row)


    @classmethod
    def get_with_id(cls, id):
        return cls.query.get(id)


    @classmethod
    def delete(cls, id_list):
        if len(id_list) < 1:
            return 0

        result = (cls.query
            .filter(cls.id.in_(id_list))
            .delete(synchronize_session=False))
        return result


    @classmethod
    def get_page(cls, page, size, search = None):
        query = cls.query

        if search:
            query = cls._filter_search(query, search)

        if 'order_num' in cls.__table__.columns:
            query = query.order_by(cls.order_num)
        else:
            query = query.order_by(desc(cls.id))

        return (query.paginate(page, per_page = size, error_out = False))

    @classmethod
    def get_all(cls):
        return cls.query.all()
        
    @classmethod
    def get_count(cls, search = None):
        result = db.session.query(func.count(cls.id))

        if search:
            result = cls._filter_count(result, search)
        
        return result.scalar()

    @classmethod
    def from_dict(cls, values):
        inst = cls()

        for c in cls.__table__.columns:
            v = values.get(c.name)

            if v is not None and v != '':
                setattr(inst, c.name, v)
        return inst
    
    def to_dict(self):
        d = DotDict()

        for c in self.__table__.columns:
            v = getattr(self, c.name)

            if v is not None:
                d[c.name] = v
        return d

    @classmethod
    def _filter_search(cls, query, search):
        # do nothing filter
        return query

    @classmethod
    def _filter_count(cls, query, search):
        # do nothing filter
        return query
