# coding:utf-8

def _before_request():
    pass

def _after_request(response):
    # app.logger.info(response)
    return response

def init_interceptor(app):
    app.before_request(_before_request)
    app.after_request(_after_request)
