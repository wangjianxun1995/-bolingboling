from flask import current_app, jsonify
from flask import make_response
from flask import request

from info import constants
from info import redis_store
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
    # current_app.logger.info(text)


    response= make_response(image)

    response.headers['Content-Type']='image/jpeg'

    return  response
    # return image

