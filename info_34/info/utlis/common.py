from flask import current_app
from flask import g
from flask import session




def do_index_kind(li):
    if li == 0:
        return "first"
    elif li == 1:
        return "second"
    elif li == 2:
        return "third"
    else:
        return ""

import functools
def login_user_data(f):
    # 作用就是 保留原有的函数的参数设置，
    # 不会被wrapper修改
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        user_id = session.get('user_id')
        user = None
        if user_id:

            # 如果 有值说明用户已经登录
            from info.models import User
            user = User.query.get(user_id)

        g.user=user
        return f(*args, **kwargs)
    return wrapper