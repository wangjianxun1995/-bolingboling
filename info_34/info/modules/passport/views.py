import re

from datetime import datetime
from flask import current_app, jsonify
from flask import make_response
from flask import request
from flask import session

from info import constants, db
from info import redis_store
from info.lib.yuntongxun.sms import CCP
from info.models import User
from info.response_code import RET
from info.utlis.captcha.captcha import captcha
from info.modules.passport import passport_blue
@passport_blue.route('/image_code')
def get_image_code():

    code_id = request.args.get('code_id')
    name,text,image = captcha.generate_captcha()

    try:
        redis_store.setex('img_'+ code_id,constants.IMAGE_CODE_REDIS_EXPIRES,text)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DATAERR,errmsg='redis保存失败')

    current_app.logger.info(text)


    response= make_response(image)

    response.headers['Content-Type']='image/jpeg'

    return  response
    # return image

@passport_blue.route('/sms_code',methods=['POST'])
def send_sms_code():
    data = request.json
    mobile=data.get('mobile')
    image_code =data.get('image_code')
    image_code_id = data.get('image_code_id')
    if not all([mobile,image_code,image_code_id]):
        return jsonify(errno = RET.PARAMERR,errmsg ='参数不正确')
    if not re.match(r'1[3-9][0-9]{9}',mobile):
        return jsonify(errno = RET.PARAMERR,errmsg ='手机格式不正确')
    count =User.query.filter(User.mobile == mobile).count()
    if count > 0:
        return jsonify(errno=RET.DATAEXIST,errmsg='手机号已经注册')
    try:
        redis_code =redis_store.get('img_'+image_code_id)
        if redis_code:
            redis_code =redis_code.decode()
            redis_store.delete('img_'+image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg = 'redis数据有问题')
    if not redis_code:
        return jsonify(errno=RET.DATAERR,errmsg = '图片验证码以及过期')
    if image_code.lower() != redis_code.lower():
        return jsonify(errno=RET.DATAERR,errmsg = '验证码不一致')
    from random import randint
    sms_code = '%06d'%randint(0,999999)
    result = CCP().send_template_sms(mobile,[sms_code,constants.SMS_CODE_REDIS_EXPIRES/60],1)
    # if result !=0:
        #return jsonify(errno=RET.DATAERR,errmsg = '发送失败')
    try:
        redis_store.setex('sms_'+mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
    except Exception as e:
        current_app.logger.error(e)
        return  jsonify(errno=RET.DATAERR,errmsg = '发送失败')
    return  jsonify(errno=RET.OK,errmsg = 'OK')

# 注册后端
@passport_blue.route('/register',methods=['POST'])
def register():
    json_data = request.json
    mobile = json_data.get('mobile')
    sms_code = json_data.get('sms_code')
    password= json_data.get('password')
    if not all([mobile,sms_code,password]):
        return jsonify (errno = RET.PARAMERR,errmsg='参数不全')

    try:
        redis_sms_code = redis_store.get('sms_'+mobile)
        if redis_sms_code:
            redis_sms_code = redis_sms_code.decode()
            redis_store.delete('sms_'+mobile)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg='数据有误')

    if not redis_sms_code:
        return jsonify(errno = RET.NODATA,errmsg ='短信验证码过期 ')

    if redis_sms_code !=sms_code:
        return jsonify(errno = RET.DATAERR,errmsg='验证码不一致')

    user = User()
    user.mobile= mobile
    user.password = password
    user.nick_name = mobile

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.app.logger.error(e)
        db.session.rollback()

    session['user_id']= user.id
    session['mobile'] = mobile
    session['nick_name']= user.nick_name

    return jsonify(errno =RET.OK,errmsg='注册成功')

@passport_blue.route('/login',methods=['POSt'])
def login():
   #1.后端要接收的数据
    json_data=request.json
    mobile = json_data.get('mobile')
    password = json_data.get('password')
   #2.判断数据是否齐全
    if not all([mobile,password]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数不全 ')
    # 根据用户名查询用户记录
    try:
        user =User.query.filter(User.mobile==mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='数据库错误 ')
#进行查询的时候user 有可能没有值
    if not user:
        return jsonify(errno=RET.USERERR,errmsg='暂未注册')
#如果有记录说明已经注册过，判断密码是否正确
   # check_passowrd 密码正确返回true
   #check_passowrd 密码不正确返回false
    if not user.check_passowrd(password):
        return jsonify(errno =RET.PWDERR,errmsg='用户名或者密码错误 ')
#正确，记录登录信息
    session['user_id']=user.id
    session['nick_name']=user.nick_name
    session['mobile'] =user.mobile

    user.last_login = datetime.now()

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.roolback()
    return jsonify(errno=RET.OK,errmsg='ok')

@passport_blue.route('/logout',methods=['POST'])
def logout():
    session.pop('user_id',None)
    session.pop('nick_name',None)
    session.pop('mobile',None)

    return   jsonify(errno=RET.OK,errmsg='OK')






