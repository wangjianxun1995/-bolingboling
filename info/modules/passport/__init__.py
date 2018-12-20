from flask import Blueprint

passport_blue=Blueprint('passport',__name__,url_prefix='/passport')

from . import views
# @passport_blue.route('/image_code')
# def get_image_code():

#     return 'image_code'