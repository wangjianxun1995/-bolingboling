from flask import Blueprint

news_blue_list=Blueprint('news',__name__,url_prefix='/news')

from . import views_blue