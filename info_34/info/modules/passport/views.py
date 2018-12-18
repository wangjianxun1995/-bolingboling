import re
from flask import current_app, jsonify
from flask import make_response
from flask import request

from info import constants
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