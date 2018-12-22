from flask import abort
from flask import current_app, jsonify
from flask import g
from flask import render_template
from flask import request
from flask import session

from common import login_user_data
from info import db
from info.models import  News, Comment
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
        abort(404)
        return jsonify(errno=RET.NODATA,errmsg='没有这个新闻！')

    if news is None:
        abort(404)
        return jsonify(errno=RET.NODATA, errmsg='没有这个新闻！')

    #######################################判断用户是否收藏按钮##########################################
    is_collected =False
    if user:
        if news in user.collection_news:
            is_collected = True

    data = {
        'user_info': user.to_dict() if user else None,
        'clisks_news': clicks_news,
        'news':news.to_dict()
    }
    # return '%s'% news_id
    return render_template('news/detail.html',data=data)


"""

点击收藏的需求 ：  因为收藏和取消收藏 传递的数据是一样的 只不过行为不一样 ，
所以我们定义一个 参数 action: 值就是2个 一个是 收藏 一个是 取消收藏

1. 收藏必须是登陆用户才可以调用
2. 接收前端提交的数据
3. 校验数据
    3.1 news_id
    3.2 action
4. 根据用户的行为 进行业务逻辑的实现
5. 更新数据
6. 返回相应

"""
@news_blue_list.route('/news_collect',methods =['post'])
@login_user_data
def news_collect():
    # 1.收藏必须是登陆用户才可以调用
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
    # 2. 接收前端提交的数据(json)
    news_id = request.json.get('news_id')  # 新闻id
    action = request.json.get('action')   # 行为
    # 3. 校验数据
    #     3.1 news_id 判断词条信息必须有  （查询数据库）
    if news_id is None:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    try:
        news =News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询失败')
    if not news:
        return jsonify(errno=RET.NODATA, errmsg='没有此条数据')

    #     3.2 action
    if action not in ["cancel_collect", "collect"]:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 4. 根据用户的行为 进行业务逻辑的实现
    if action =='collect':
        #收藏
        # 收藏了 就不能在收藏了（1.先根据新闻的id进行以下查询如果有 说明已经收藏过了
        # ，如果没有查询到说明没有收藏）
        if news not in user.collection_news:
            user.collection_news.append(news)
    else:
        # 取消收藏
        if news in user.collection_news:
            user.collection_news.remove(news)
    # 5. 更新数据
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()

    # 6. 返回相应
    return jsonify(errno=RET.OK, errmsg='操作成功')

@news_blue_list.route('/news_comment',methods=['POST'])
@login_user_data
def news_comment():

    # 1. 这个试图必须是登陆用户才可以访问
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
    # 2. 要接收参数， news_id, content
    news_id = request.json.get('news_id')
    content = request.json.get('comment')
    comments_id = request.json.get('parent_id')
    # 3. 2个参数必须有，
    if not all([news_id,content]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不全')
    # 4. 判断 news 必须存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询失败')
    if not news:
        return jsonify(errno=RET.NODATA, errmsg='未查询到此新闻')
    # 5. 数据入库
    comment = Comment()
    comment.user_id = user.id
    comment.news_id = news.id
    comment.content = content
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
    # 6. 返回响应 同时把 新增的数据传递给前端
    return jsonify(errno=RET.OK, errmsg='OK',data ={'comment':comment.to_dict()})

