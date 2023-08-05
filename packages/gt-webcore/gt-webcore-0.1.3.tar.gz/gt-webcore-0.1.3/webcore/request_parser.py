# coding:utf-8
from flask_restful import reqparse

def parse_args(params_list, req=None):
    parser = reqparse.RequestParser()

    for param in params_list:
        parser.add_argument(**param)

    return parser.parse_args(req)

def parse_custom_args(params_list, arg):
    if not arg:
        return None

    for param in params_list:
        param.location = 'data'
        
    if isinstance(arg, list):
        args = []

        for item in arg:
            custom_req = reqparse.Namespace(data = item)
            args.append(parse_args(params_list, custom_req))
        
        return args
    else:
        custom_req = reqparse.Namespace(data = arg)
        return parse_args(params_list, custom_req)
       