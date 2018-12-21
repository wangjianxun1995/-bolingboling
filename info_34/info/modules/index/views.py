from flask import current_app, jsonify
from flask import render_template
from flask import request
from flask import session

from info.models import User, News, Category
from info.modules.index import index_blue
from info.response_code import RET


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

###################################以下是分类信息###################################################

    try:
        categories = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
    # 把查询的对象 列表转换为 字典列表
    categories_list= []
    for item in categories:
        categories_list.append(item.to_dict())



    data={
        'user_info':user.to_dict() if user else None,
        'clisks_news':clicks_news,
        'categories':categories_list
    }

    return render_template('news/index.html',data=data)

@index_blue.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news_blue/favicon.ico')

@index_blue.route('/news_list')
def get_index_list():
    # 获取值
    params= request.args

    cid = params.get('cid','1')
    page = params.get('page',1)
    per_page =params.get('per_page',20)

    try:
        page=int(page)
        per_page=int(per_page)
    except Exception as e:
        page = 1
        per_page = 20

    """
       category_id = 1 的为最新数据 数据库
       中 其实是没有最新数据的新闻的我们是
       根据新闻的时间来获取最新的新闻
    """
    filter=[]
    if cid !='1':
        filter.append(News.category_id==cid)


    # 查询数据
    try:
        paginate = News.query.filter(*filter).order_by(News.create_time.desc()).paginate(page=page,per_page=per_page)
        # 获取 所有当前分页的数据
        news = paginate.items
        # 总页数
        total_page = paginate.pages
        # 当前页数
        current_page = paginate.page
    except Exception as e:
        current_app.logger.error(e)
        return  jsonify(errno = RET.NODATA,errmsg = '数据查询失败')
    news_list = []
    for item in news:
        news_list.append(item.to_basic_dict())
    return jsonify(errno = RET.OK,errmsg ='OK',
                   news_list=news_list,
                   current_page= current_page,
                   cid=cid,
                   total_page=total_page)
