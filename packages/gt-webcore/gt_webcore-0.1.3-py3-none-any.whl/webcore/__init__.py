# -*- coding: utf-8 -
from flask_sqlalchemy import SQLAlchemy
from .gt_flask import GtFlask
from .constant import VERSION
import logging.config
import os
import importlib

def create_log_path(log_path):
    """
    文件日志不会自动生成目录，只能先自行创建，否则日志报错
    """
    if not os.path.exists(log_path):
        os.makedirs(log_path)

def create_app(config):
    create_log_path(config.LOGGER_CONFIG['path'])
    logging.config.dictConfig(config.LOGGER_CONFIG)
    global app
    app = GtFlask(__name__)
    app.logger.info('---基础框架正在初始化中, 框架版本:V{}---'.format(VERSION))
    app.init_app()
    app.config.from_object(config)

    app.logger.info('初始化数据库...')
    db = SQLAlchemy(app)
    app.db = db

    if config.MODULES:
        load_modules(config.MODULES)
    
    return app

def load_modules(modules):
    app.logger.info('开始加载模块...')

    for module in modules:
        name = module['name']
        app.logger.info('加载模块：{}'.format(name))

        try:
            inst = importlib.import_module(name, module['package'])
            init_app = getattr(inst, 'init_app')
            init_app(app)
        except:
            app.logger.error('Load Module [{}] Error.'.format(name), exc_info = True)
