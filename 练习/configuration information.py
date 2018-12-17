from redis import StrictRedis
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask.ext.wtf import CSRFProtect
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand



app = Flask(__name__)
# db = SQLAlchemy(app)
class Config(object):
    SECRET_KEY='DASDASDWQEQEQWDASDASDDCCKKHIFH'
    DEBUG =True
    # 设置数据库
    SQLALCHEMY_DATABASE_URI ='mysql://root:mysql@127.0.0.1:3306/ww'
    # app.config.setdefault('SQLALCHEMY_DATABASE_URI','mysql://root:mysql@127.0.0.1:3306/ww')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 设置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 设置session
    SESSION_TYPE ='redis'  # 选择存储 session 数据的库
    # 指定1 号库
    SESSION_REDIS=StrictRedis(host=REDIS_HOST,port=REDIS_PORT,db=1)
    #  是否对cookie信息进行加密处理，修改为True，必须要设置secret_key
    SESSION_USE_SIGNER =True
    # 设置session的有效期 单位秒
    PERMANENT_SESSION_LIFETIME = 3600
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# 提交配置信息
app.config.from_object(Config)
#创建sql实例对象
db =SQLAlchemy(app)
# csrf 的 设置
CSRFProtect(app)

Session(app)

manger = Manager(app)
Migrate(app=app,db=db)
manger.add_command('db',MigrateCommand)
@app.route('/')
def world():
    return 'hello'


if __name__ == '__main__':
    manger.run()