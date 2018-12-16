from flask import Flask
from flask.ext.session import Session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import CSRFProtect
from redis import StrictRedis

from config import Config

app=Flask(__name__)


app.config.from_object(Config)
db = SQLAlchemy(app)
    #设置 redis数据库
sr = StrictRedis(host=Config.REDIS_HOSt,port=Config.REDIS_PORT)

#设置CSRf
CSRFProtect(app)

# 设置session
Session(app)