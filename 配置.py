from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis,Redis # 他俩一样
from flask_wtf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from flask_migrate import  Migrate,MigrateCommand
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
manger = Manager(app)
Migrate(app=app,db=db)
manger.add_command('db',MigrateCommand)
@app.route('/')
def world():

    return 'hello'

if __name__ == '__main__':
    manger.run()