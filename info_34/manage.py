from flask import current_app
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from info import create_app,db
from info import models
# from info import views
from info.models import User
from info.utlis.common import do_index_kind

# StrictRedis ,Redis是一样的

app = create_app()

app.add_template_filter(do_index_kind, "index_kind")
from info.modules.news_blue import news_blue_list
app.register_blueprint(news_blue_list)

#使用 Manager管理类来管理 app
manager=Manager(app)

Migrate(app=app,db=db)
#将迁移指令添加到 manager中
manager.add_command('db',MigrateCommand)
@manager.option('-n', '-name', dest='name')
@manager.option('-p', '-password', dest='password')
def createsuperuser(name, password):
    """创建管理员用户"""
    if not all([name, password]):
        print('参数不足')
        return

    user = User()
    user.mobile = name
    user.nick_name = name
    user.password = password
    user.is_admin = True

    try:
        db.session.add(user)
        db.session.commit()
        print("创建成功")
    except Exception as e:
        print(e)
        db.session.rollback()


if __name__ == '__main__':
    # app.run()
    manager.run()
