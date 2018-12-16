from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis,Redis # 他俩一样
from flask_wtf import CSRFProtect
from flask_session import Session
from flask_script import Manager

app=Flask(__name__)

class Config():
    SECRET_KEY = 'KZtgoZECnZyp/hiU49YHotf2Nv4IGYqF5I7M6K3iClzvTWYtALha9E2i7wgIK78X'
    DEBUG = True
    # 设置mysql数据库
    SQLALCHEMY_DATABASE_URI ='mysql:root:mysql@127.0.0.1:3306/wang_sql'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # app.config['SQLALCHEMY_DATABASE_YRI']='mysql:root:mysql@127.0.0.1:3306/wang_sql'

    REDIS_HOSt = '127.0.0.1'
    REDIS_PORT =6379
    SESSION_TYPE  = 'redis'
    SESSION_REDIS = StrictRedis(host=REDIS_HOSt,port=REDIS_PORT,db = 1)
    SESSION_USE_SIGNER =True
    PERMANENT_SESSION_LIFETIME = 3600
app.config.from_object(Config)
db = SQLAlchemy(app)
    #设置 redis数据库
sr = StrictRedis(host=Config.REDIS_HOSt,port=Config.REDIS_PORT)

#设置CSRf
CSRFProtect(app)

# 设置session
Session(app)
manger = Manager(app)
@app.route('/')
def world():

    return 'hello'

if __name__ == '__main__':
    manger.run()