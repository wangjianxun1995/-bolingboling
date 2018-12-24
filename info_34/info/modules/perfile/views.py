from flask import current_app
from flask import g, jsonify
from flask import render_template
from flask import request
from flask import session
from common import login_user_data
from image_storage import storage
from info import constants
from info import db
from info.modules.perfile import  profile_blu
from info.response_code import RET


@profile_blu.route('/info')
@login_user_data
def user_info():
    user = g.user
    # 返回 user的首页展示 以及登录信息的展示 和html的抽取
    return render_template('news/user.html',data = {'user_info': user.to_dict() if user else None})
##########################################修改个人信息######################################################

@profile_blu.route('/base_info',methods=(['POST','GET']))
@login_user_data
def user_base_info():
    user=g.user
    if user is None:
        return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
    if request.method == 'GET':
        return render_template('news/user_base_info.html',data = {'user_info':user.to_dict() if user else None})
    """
       修改数据

       1. 接收数据
       2. 校验数据
       3. 更新数据
       4. 返回相应
    """
    # 1. 接收数据
    parameter_info = request.json
    nick_name =parameter_info.get('nick_name') #姓名
    gender = parameter_info.get('gender')# 性别
    signature = parameter_info.get('signature')# 个性签名
    # 2. 校验数据
    if not all([nick_name,signature,gender]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    if gender not in['MAN',"WOMAN"]:
        return jsonify(errno=RET.PARAMERR, errmsg='性别错误')

    # 3. 更新数据,并保存数据
    user.nick_name = nick_name
    user.gender = gender
    user.signature =signature
    try:
        db.session.commit()

    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
    # 实时更新保存的数据
    session['nick_name'] = nick_name

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
    # 4. 返回相应
    return jsonify(errno=RET.OK, errmsg='Ok')
##########################################修改头像######################################################

@profile_blu.route('/pic_info',methods=['POST','GET'])
@login_user_data
def user_pic_info():
    user = g.user
    if user is None:
        return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
    if request.method == "GET":
        return render_template('news/user_pic_info.html',data={'user_info':user.to_dict() if user else None})

    """
       POST 上传图片

       1. 接收数据( 图片 )
       2. 上传到七牛云中 ,获取到 返回的图片名字
       3. 更新用户的头像信息
       4. 返回相应
    """
    # 1. 接收数据( 图片 )
    avatar = request.files.get('avatar')
    if not avatar:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 2. 上传到七牛云(读取图片的二进制) ,获取到 返回的图片名字
    try:
        # read 方法 去读取数据
        data = avatar.read()
        #  然后调用七牛云的存储image_storage 的 storaged 方法
        parh = storage(data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传失败')
    # 3. 更新用户的头像信息
    user.avatar_url = parh
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
    # 4. 返回相应

    return jsonify(errno=RET.OK, errmsg='上传成功',data={'avatar_url':constants.QINIU_DOMIN_PREFIX+parh})
##########################################修改密码######################################################

    '''

    # GET :展示数据
    #
    # POST: 修改密码
    # 1. 接收参数
    # 2. 三个参数必须都有
    # 3. 两次密码必须一致
    # 4. 查询用户 当前的密码输入是否正确
    # 5. 修改密码
    # 6. 返回相应

    '''
@profile_blu.route('/pass_info', methods=["GET", "POST"])
@login_user_data
def pass_info():

    #GET :展示数据
    user = g.user
    if user is None:
        return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录 ')
    if request.method == 'GET':
        return render_template('news/user_pass_info.html')
    # POST: 修改密码

    # 1. 接收参数
    old_password=request.json.get('old_password')
    new_password = request.json.get('new_password')
    new_password2 = request.json.get('new_password2')
    # 2. 三个参数必须都有
    if not all([old_password,new_password,new_password2]):
        return jsonify(errno=RET.PARAMERR, errmsg='数据错误')
    # 3. 两次密码必须一致
    if not new_password2 == new_password:
        return jsonify(errno=RET.PWDERR, errmsg='密码不一致')
    # 4. 查询用户 当前的密码输入是否正确
    if not user.check_passowrd(old_password):

        return jsonify(errno=RET.PWDERR, errmsg='请输入正确的原始密码')
    # 5. 修改密码
    user.password =new_password
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
    # 6. 返回相应
    return jsonify(errno=RET.OK, errmsg='修改成功')
##############################################以下是我的收藏列表##############################################################################
@profile_blu.route('/collection')
@login_user_data
def user_collection():

    return render_template('news/user_collection.html')