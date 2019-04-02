from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session,
    send_from_directory,
    abort,
)

from models.user import User

main = Blueprint('user', __name__)

from utils1 import encryption
from utils1 import log
from utils1 import salt

from werkzeug.utils import secure_filename
import os
from config import user_file_director

from models.topic import Topic
from models.reply import Reply

import uuid
csrf_token = {}


def current_user():
    username = session.get('username', '[游客]')
    return username


@main.route('/')
def index():
    username = current_user()
    print('username:', username)
    return render_template('user/index.html', username=username)


@main.route('/<int:user_id>')
def profile(user_id):
    user = User.findBy(id=user_id)

    print('user_id:', user_id)
    token = str(uuid.uuid4())
    csrf_token[token] = user_id
    print('**token:', token)
    created_topic = Topic.findAll(user_id=user_id)
    join_topic = Reply.findAll(author_id=user_id)
    return render_template('user/profile_look.html',
                           user=user,
                           created_topic=created_topic,
                           join_topic=join_topic,
                           token=token)
# 这里的 id 转换还没有完成
# @main.route('/<user_id>')
# def profile(user_id):
#     user = User.findBy(_id=user_id)
#
#     print('user_id:', user_id, user)
#     token = str(uuid.uuid4())
#     csrf_token[token] = user_id
#     print('**token:', token)
#     created_topic = Topic.findAll(user_id=user.id)
#     join_topic = Reply.findAll(author_id=user.id)
#     return render_template('user/profile_look.html',
#                            user=user,
#                            created_topic=created_topic,
#                            join_topic=join_topic,
#                            token=token)

@main.route('/delete')
def delete():
    user_id = int(request.args.get('user_id', -1))
    topic_id = int(request.args.get('topic_id', -1))

    username = current_user()
    user = User.findBy(username=username)

    token = request.args.get('token', -1)
    if token in csrf_token and csrf_token[token] == user_id and user_id == user.id:
        Topic.deleteById(topic_id)
        created_topic = Topic.findAll(user_id=user_id)
        join_topic = Reply.findAll(author_id=user_id)
        csrf_token.pop(token)
        return render_template('user/profile_look.html',
                               user=user,
                               created_topic=created_topic,
                               join_topic=join_topic,
                               token=token)
    else:
        abort(404)


@main.route('/register')
def register():
    log('** register 函数')
    return render_template('user/register.html')


@main.route('/register_infor', methods=["POST"])
def register_infor():
    form = request.form
    print('regiter status and form:', User.register_check(form), form)
    if User.register_check(form):
        u = User.new(form)
        # u = User()
        # u.from_form(form)
        # u.save()
        link = '注册成功！'
        return render_template('user/register.html', infor=link)
    else:
        warns = '用户名或密码长度必须大于 2，请重新注册！'
        return render_template('user/register.html', infor=warns)


@main.route('/login')
def login():
    return render_template('user/login.html')


@main.route('/login_infor', methods=["POST"])
def login_infor():
    form = request.form
    if User.login_check(form):
        username = form['username']
        session['username'] = username
        session.permanent = True
        return redirect(url_for('.index'))
    else:
        warns = '登录失败，请重新登录！'
        return render_template('user/login.html', infor=warns)

@main.route('/logout')
def logout():
    session['username'] = '[游客]'
    return redirect(url_for('.index'))

@main.route('/login_infor')
def login_infors():
    warns = '登录失败，请重新登录！'
    return render_template('user/login.html', infor=warns)

@main.route('/profile')
def user_profile():
    username = current_user()
    user = User.findBy(username=username)
    if user is not None:
        return render_template('user/profile.html', user=user)
    else:
        return redirect(url_for('.login'))


@main.route('/upload', methods=['POST'])
def user_upload():
    username = current_user()
    user = User.findBy(username=username)
    user_id = user.id
    if username != '[游客]':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_file_director, filename))
        User.update(user_id, avatar_path=filename)

    return redirect(url_for('.user_profile'))





