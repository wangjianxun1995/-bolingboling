from redis import StrictRedis


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

# 线上环境
class On_line(Config):
    DEBUG = False

# 线下环境
class Off_line(Config):
    DEBUG = True

config = {
    'on-line':On_line,
    'off-line':Off_line
}