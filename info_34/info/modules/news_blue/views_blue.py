from flask import abort
from flask import current_app, jsonify
from flask import g
from flask import render_template
from flask import request
from flask import session

from common import login_user_data
from info import db
from info.models import  News, Comment, CommentLike
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
    is_collected =False   # false 是都没有收藏 true  是收藏
    is_followed = False   # false是没有关注 true 是关注
    if user:
        if news in user.collection_news:
            is_collected = True
        try:
            news_user = User.query.get(news.user_id)
        except Exception as e:
            current_app.logger.error(e)
        if news_user in user.followers:
            is_followed = True
    #######################################以下为当前新闻的所有评论##############################

    try:
        comments = Comment.query.filter(Comment.news_id == news_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)
    # 在这里查询 Comment_Like 中的当前登录用户的id 信息
    if user:
        try:
            comment_like_list = CommentLike.query.filter(CommentLike.user_id==user.id).all()
        except Exception as e:
            current_app.logger.error(e)
        # 将对象转换为列表
        user_comment_like_ids = []
        for i in comment_like_list:
            user_comment_like_ids.append(i.comment_id)

    comments_list= []
    for item in comments:
        comment_dict = item.to_dict()
        # 我们的自己判断 当前用户是否对这个评论 点赞
        comment_dict['is_like'] = False
        if user and item.id in user_comment_like_ids:
            comment_dict['is_like'] = True
        comments_list.append(comment_dict)

    data = {

        'user_info': user.to_dict() if user else None,
        'clisks_news': clicks_news,
        'news':news.to_dict(),
        'comments':comments_list,


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
    parent_comment_id = request.json.get('parent_id')
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
    # 根据用户传递过来的 评论的父ID 来判断用户是否跟帖
    # 如果parent_comment_id有值则是跟帖
    if parent_comment_id:
        comment.parent_id = parent_comment_id

    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
    # 6. 返回响应 同时把 新增的数据传递给前端
    return jsonify(errno=RET.OK, errmsg='OK',data ={'comment':comment.to_dict()})
'''
点赞的需求：
    需要将 用户信息， 评论的id 传递给后端 点赞的状态 传递给后端


1. 点赞功能必须要登陆
2. 接收参数 ，并且对参数进行判断
3. comment_id 进行查询，并且判断 必须有评论
4. 数据入库
5. 返回相应

'''

@news_blue_list.route('/comment_like',methods=['post'])
@login_user_data
def comment_like():
    # 1.点赞功能必须要登陆
    user = g.user
    if user is None:
        return jsonify(errno=RET.SESSIONERR, errmsg='您未登录')
    # 2.接收参数 ，并且对参数进行判断
    comment_id = request.json.get('comment_id')
    action = request.json.get('action')
    if not all([comment_id,action]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不正确')
    # 3. comment_id 进行查询，并且判断 必须有评论
    try:
        comment = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='未查询此评论')
    # 4. 数据入库
    if action == 'add':
        comment_like = CommentLike.query.filter(CommentLike.comment_id==comment_id
                                                ,CommentLike.user_id == user.id).first()
        if not comment_like:
            cl = CommentLike()
            cl.comment_id=comment_id
            cl.user_id = user.id

            # 更新 点赞 的数量
            comment.like_count += 1

            try:
                db.session.add(cl)
                db.session.commit()
            except Exception as e:
                current_app.logger.error(e)
                db.session.rollback()
    else:
        #取消 点赞
        # 先查询 有没有点赞
        comment_like = CommentLike.query.filter(CommentLike.comment_id == comment_id
                                                , CommentLike.user_id == user.id).first()
        # 如果点赞了 才取消
        # 把 点赞数量 -1
        if comment_like:
            comment.like_count -= 1
            try:
                db.session.delete(comment_like)
                db.session.commit()
            except Exception as e:
                current_app.logger.error(e)
                db.session.rollback()


    # 5. 返回相应
    return jsonify(errno=RET.OK, errmsg='Ok')

