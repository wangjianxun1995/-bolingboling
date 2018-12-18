import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from redis import StrictRedis
from config import config

"""
http://140.143.37.139:4999/
https://gitee.com/
https://gitee.com/itcastitheima/info_34.git
"""
db = SQLAlchemy()

redis_store=None

# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:mysql@127.0.0.1:3306/info_34'
def create_app(config_name='development'):
    #日志
    setup_log(config_name)

    app=Flask(__name__)
    # config['development']   DevelopmentConfig
    # config['production']  ProductionConfig

    #加载配置文件
    app.config.from_object(config[config_name])

    #创建SQLAlchemy 实例对象
    # db=SQLAlchemy(app)
    db.init_app(app)

    #创建Redis实例
    # sr=StrictRedis(host='192.168.23.5',port=6379)
    """
    在函数外边是一个作用域
    在函数内部是一个作用域
    我们想在函数内部使用函数外部的变量： 使用 global
    """
    global redis_store
    redis_store=StrictRedis(host=config[config_name].REDIS_HOST,port=config[config_name].REDIS_PORT)

    # CSRF的设置 -- 关于原理我们明天将
    CSRFProtect(app)

    """
    session是保存在 服务器端
        session(s 小写开头)默认是保存在cookie中的
        所以 小写的session 不能满足我们的需求
        这个时候我们用 大写的Session

    cookie是保存在 浏览器端


    Session
        SESSION_REDIS: 因为我们要将数据保存在 Redis-Server 中，所以我们要连接redis-server
                    连接redis-server 就要有一个客户端
        SESSION_KEY_PREFIX: session数据的前缀，默认是 session:
        SESSION_USE_SIGNER:     session是依赖于cookie的， cookie数据是否进行加密处理
                            是否对我们的cookie数据进行加密的签名处理
        PERMANENT_SESSION_LIFETIME:  设置Session数据的有效期 单位为秒数
    """

    Session(app)

    from info.modules.index import index_blue

    app.register_blueprint(index_blue)

    #一定要注意：返回
    return app


def setup_log(config_name):
    """配置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

