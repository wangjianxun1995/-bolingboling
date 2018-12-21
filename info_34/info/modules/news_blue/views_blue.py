from flask import current_app, jsonify
from flask import g
from flask import render_template
from flask import session

from common import login_user_data
from info.models import  News
from info.modules.news_blue import news_blue_list
from info.response_code import RET
from info.models import  User

@news_blue_list.route('/<int:news_id>')
@login_user_data
def detail(news_id):
    # # 因为登录信息保存在session中，所以获取user_id
    #
    # user_id = session.get('user_id')
    # user = None
    # if user_id:
    #     try:
    #         # 如果 有值说明用户已经登录
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)

    user = g.user
#######################################点击率排行##########################################

    # 根据点击率 进行指定数量降序 排列
    try:
        click_list = News.query.order_by(News.clicks.desc()).limit(10)
    except Exception as e:
        current_app.logger.error(e)

    clicks_news = []
    for item in click_list:
        clicks_news.append(item.to_dict())
#######################################以下是根据新闻id，查询详细分类信息##########################################
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.NODATA,errmsg='没有这个新闻！')

    if news is None:
        return jsonify(errno=RET.NODATA, errmsg='没有这个新闻！')




    data = {
        'user_info': user.to_dict() if user else None,
        'clisks_news': clicks_news,
        'news':news.to_dict()
    }
    # return '%s'% news_id
    return render_template('news/detail.html',data=data)