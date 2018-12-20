from flask import current_app
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from info import create_app,db
from info import models
# from info import views

# StrictRedis ,Redis是一样的
"""
manage.py 其实主要是让我们的工程 运行起来
至于一些配置 和初始化的设置 我们都放到 info package 中
info 是我们进行业务逻辑处理的文件夹
"""
app = create_app()

#使用 Manager管理类来管理 app
manager=Manager(app)

Migrate(app=app,db=db)
#将迁移指令添加到 manager中
manager.add_command('db',MigrateCommand)



if __name__ == '__main__':
    # app.run()
    manager.run()
