from flask import current_app
from flask import render_template

from info_34.info.modules.index import index_blue

@index_blue.route('/')
def index():
    return render_template('news/index.html')

@index_blue.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')