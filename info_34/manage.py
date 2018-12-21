from flask import current_app
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from info import create_app,db
from info import models
# from info import views
from info.utlis.common import do_index_kind

# StrictRedis ,Redis是一样的

app = create_app()

app.add_template_filter(do_index_kind, "index_kind")

#使用 Manager管理类来管理 app
manager=Manager(app)

Migrate(app=app,db=db)
#将迁移指令添加到 manager中
manager.add_command('db',MigrateCommand)



if __name__ == '__main__':
    # app.run()
    manager.run()
