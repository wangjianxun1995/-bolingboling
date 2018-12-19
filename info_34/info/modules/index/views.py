from flask import current_app
from flask import render_template
from flask import session

from info.models import User
from info.modules.index import index_blue

@index_blue.route('/')
def index():
    # 因为登录信息保存在session中，所以获取user_id

    user_id  =session.get('user_id')
    user = None
    if user_id:
        try:
            # 如果 有值说明用户已经登录
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    data={
        'user_info':user.to_dict() if user else None
    }

    return render_template('news/index.html',data=data)

@index_blue.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')