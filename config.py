# 配置文件类
import logging
from redis import StrictRedis


class Config(object):
    # 默认日志等级
    LOG_LEVEL = logging.DEBUG

    #secret_key
    SECRET_KEY='KZtgoZECnZyp/hiU49YHotf2Nv4IGYqF5I7M6K3iClzvTWYtALha9E2i7wgIK78X'

    DEBUG=True
    #Mysql的配置信息
    SQLALCHEMY_DATABASE_URI='mysql://root:mysql@127.0.0.1:3306/info_34'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    #设置Redis
    REDIS_HOST='127.0.0.1'
    REDIS_PORT=6379

    # 设置 Session的配置信息
    SESSION_TYPE='redis'
    SESSION_REDIS=StrictRedis(host=REDIS_HOST,port=REDIS_PORT,db=1)
    SESSION_USE_SIGNER=True  # 修改为True之后就必须要是何止 serect_key
    PERMANENT_SESSION_LIFETIME = 3600

"""
封装
继承
多态
"""
# 开发环境
class DevelopmentConfig(Config):

    DEBUG = True


# 生成环境
class ProductionConfig(Config):
    DEBUG = False

#定义一个字典
config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig
}
