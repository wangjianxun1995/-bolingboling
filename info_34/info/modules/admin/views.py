from flask import render_template

from info.modules.admin import admin_blu
# 后台首页
@admin_blu.route('/',methods= ['POST','GET'])
def admin_home():
    return render_template('admin/index.html')
#后台登录页面
@admin_blu.route('/login',methods= ['POST','GET'])
def admin_login():
    return render_template('admin/login.html')