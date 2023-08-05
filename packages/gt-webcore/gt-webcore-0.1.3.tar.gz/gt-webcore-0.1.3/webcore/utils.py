# -*- coding: utf-8 -*-
import six
import string
import functools
import random
import json
import time

from dotdict import DotDict

def batch_update_key(inst,data):
    assert(inst is not None)
    for key in data:
        assert(hasattr(inst,key))
        setattr(inst,key,data[key])

def to_dict(inst,includes = [],excludes = []):
    d = dict()
    for c in inst.__table__.columns:
        if includes and c.name not in includes:
            continue
        elif excludes and c.name in excludes:
            continue
        v = getattr(inst, c.name)
        d[c.name] = v
    return d

letters =string.letters if six.PY2 else string.ascii_letters
letters  = string.digits + letters + '_-'

def base_encode(number, base):
    assert number >= 0, 'positive integer required'
    assert base <= len(letters), 'The base value is too large'
    if number == 0:
        return '0'
    code = []
    while number != 0:
        number, i = divmod(number, base)
        code.append(letters[i])
    return ''.join(reversed(code))


base36 = functools.partial(base_encode, base=36)


def random_liter(length, base):
    assert base <= len(letters), 'The base value is too large'
    liter=''
    for i in range(length):
        liter += letters[random.randint(0,base-1)]
    return liter


gen_key = functools.partial(random_liter, length=40, base=62)


def collection(request):
    try:
        lect = request.json
    except:
        if request.data:
            lect = json.loads(request.data.decode('utf-8'))
    if lect is None:
        lect = {}

    if request.form:
        lect.update(request.form.to_dict())

    if request.args:
        lect.update(request.args.to_dict())

    token = request.headers.get("access_token", None)
    if token:
        lect['_token']=token
    return lect


def lect_request(request,*arg,**kws):
    try:
        lect =request.json if request.json else {} if request.data==b'' else json.loads(request.data.decode('utf-8'))
    except:
        lect = {} if request.data==b'' else json.loads(request.data.decode('utf-8'))
    lect['token']=request.headers.get("access_token", None)
    if request.form:
        lect.update(request.form.to_dict())

    if request.args:
        lect.update(request.args.to_dict())

    if not arg and not kws:
        return lect

    args = kws
    if len(arg)>0:
        if arg[0].find(' ')==-1:
            return [lect.get(k, None) for k in arg]
        v = None if len(arg)>1 and arg[1] is None else ''
        args.update(dict.fromkeys(arg[0].split(), v))
    return {k:lect.get(k, args.get(k)) for k in args}


def filter(lets,arg,**kws):
    ret=DotDict()
    if not isinstance(lets,dict):
        return ret
    args=dict.fromkeys(arg.split(), None)
    args.update(kws)
    for k in args:
        ret[k]=lets.get(k, args.get(k))
    return ret


def atoi(a,b=1):
    if isinstance(a,int):
        return a
    else:
        try:
            if a.isdigit():
                i= int(a, 10)
            else:
                i= int(a, 16)
        except:
            i= b
        else:
            pass
            # i= b if i==0 else abs(i)
        return i

def object_dict(inst):
    d = DotDict()
    if inst is None:
        return d
    for c in inst.__table__.columns:
        v = getattr(inst, c.name)

        if v:
            d[c.name] = v
    return d


def str_to_list(value):
    if isinstance(value,list):
        return value
    elif isinstance(value,str):
        return value.strip('[').strip(']').strip(',').split(',')
    else:
        return []

def timestamp_to_datestr(value):
    if not value:
        return ''

    return time.strftime("%Y-%m-%d", time.localtime(value))
