from flask import current_app
from flask import render_template
from flask import session

from info.models import User, News
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
        #######################################点击率排行##########################################

    # 根据点击率 进行指定数量降序 排列
    try:
        click_list = News.query.order_by(News.clicks.desc()).limit(10)
    except Exception as e:
        current_app.logger.error(e)

    clicks_news= []
    for item in click_list:
        clicks_news.append(item.to_dict())




    data={
        'user_info':user.to_dict() if user else None,
        'clisks_news':clicks_news
    }

    return render_template('news/index.html',data=data)

@index_blue.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')