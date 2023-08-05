# -*- coding: utf-8 -
from flask import current_app as app
from flask import request, g
from webcore.result import Result
from webcore.constant import Error
from webcore import exception
import functools
import requests

def check_perm(action=None, resource='*'):
    """
    需要进行权限判断
    :param action: 若为none，则表示只解析不判断
    :param check: 用来验证用户有没有对其的操作权限
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            system_id = app.config['SYSTEM_ID']
            auth_url = app.config['AUTH_URL']

            if not system_id:
                raise exception.ParamsError('没有配置系统标识')

            if not auth_url:
                raise exception.ParamsError('没有配置授权服务地址')

            response = requests.post(auth_url, data = {
                'system_id': system_id,
                'token': token,
                'action': action
            })

            result = response.json()

            if result['code'] != Error.OK.value:
                raise exception.GtBaseError(result['code'], result['msg'])
            else:
                payload = result['data']

                if not payload:
                    raise exception.GtBaseError(Error.AUTHOR_ERROR, '没有访问授权')
    
                g.__dict__.update(payload)               
                return func(*args, **kwargs)

        return wrapper
    return decorator
