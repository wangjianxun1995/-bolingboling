from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
app=Flask(__name__)

class Config():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI ='mysql:root:mysql@127.0.0.1:3306/wang_sql'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # app.config['SQLALCHEMY_DATABASE_YRI']='mysql:root:mysql@127.0.0.1:3306/wang_sql'

    REDIS_HOSt = '127.0.0.1'
    REDIS_PORT =6379
sr = StrictRedis(host=Config.REDIS_HOSt,port=Config.REDIS_PORT)
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.route('/')
def world():

    return 'hello'

if __name__ == '__main__':
    app.run()