from flask import Flask
from flask.ext.session import Session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import CSRFProtect
from redis import StrictRedis

from config import config

sr =None
db = SQLAlchemy()
def creat_app(config_name='off-line'):
    app=Flask(__name__)



    app.config.from_object(config[config_name])
    db.init_app(app)

        #设置 redis数据库
    global sr
    sr = StrictRedis(host=config[config_name].REDIS_HOSt,port=config[config_name].REDIS_PORT)

    #设置CSRf
    CSRFProtect(app)

    # 设置session
    Session(app)

    return app