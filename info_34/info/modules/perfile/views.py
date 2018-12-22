from flask import g
from flask import render_template

from common import login_user_data
from info.modules.perfile import  profile_blu

@profile_blu.route('/info')
@login_user_data
def user_info():
    user = g.user
    # 返回 user的首页展示 以及登录信息的展示 和html的抽取
    return render_template('news/user.html',data = {'user_info':user.to_dict() if user else None})