from flask_script import Manager
from flask_migrate import  Migrate,MigrateCommand
from information import creat_app,db

app=creat_app()
manger = Manager(app)
Migrate(app=app,db=db)
manger.add_command('db',MigrateCommand)
@app.route('/')
def world():

    return 'hello'

if __name__ == '__main__':
    manger.run()