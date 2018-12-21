from flask import render_template

from info.modules.news_blue import news_blue_list

@news_blue_list.route('/<int:news_id>')
def detail(news_id):

    # return '%s'% news_id
    return render_template('news/detail.html',data={})