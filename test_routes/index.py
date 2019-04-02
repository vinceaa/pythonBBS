#  测试页面

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    send_from_directory,
)

from models.user import User
from config import user_file_director


main = Blueprint('index', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/haha')
def index1():
    form = {
        'username': 'gua',
        'password': 123,
    }
    form1 = {
        'username': 'gua1',
        'password': 123,
    }
    # ins = User.new(form)
    # ins1 = User.new(form1, haha=123)
    # print('所有的数据：', User.all())
    # print('找到的数据：', User.findAll(username='gua'))
    # print('找到的一条数据：', User.findBy(username='gua'))
    # print('找到的一条数据：', User.findBy(id=7))
    # print('通过 id 找到数据：', User.findBy(id=5))
    # print('删除之后的数据：', User.deleteById(3))
    d = User.update(3, usernam='ma')
    print('通过 id 更新之后的数据：', d)
    return redirect(url_for('.index'))

@main.route("/static/<filename>")
def uploads(filename):
    return send_from_directory(user_file_director, filename)




