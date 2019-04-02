from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session,
)

from models.user import User

main = Blueprint('topic', __name__)

from utils1 import encryption
from utils1 import log
from utils1 import salt

from models.board import Board
from models.topic import Topic
from models.user import User

import time



def current_user():
    username = session.get('username', '[游客]')
    return username


@main.route('/')
def index():
    username = current_user()
    user = User.findBy(username=username)
    boards = Board.all()
    # topics = Topic.all()
    topics = Topic.cache_all()
    # print('topics:', topics)
    topics.reverse()
    current_time = int(time.time())
    return render_template('topic/index.html',
                           boards=boards,
                           topics=topics,
                           current_time=current_time,
                           user=user)


@main.route('/new')
def new():
    username = current_user()
    user_id = User.userId(username)
    boards = Board.all()
    return render_template('topic/new.html',
                           user_id=user_id,
                           boards=boards)


@main.route('/add', methods=['post'])
def add():
    form = request.form
    log('话题的 form 信息:', form)
    Topic.new(form)
    return redirect(url_for('.index'))


@main.route('/detail/<int:topic_id>')
def detail(topic_id):
    topic = Topic.getByid(topic_id)
    topic.update(topic_id, views_number=topic.views_number + 1)
    username = current_user()
    user_id = User.userId(username)
    current_time = int(time.time())
    return render_template('topic/detail.html',
                           topic=topic,
                           replyer_id=user_id,
                           current_time=current_time)

@main.route('/<int:board_id>')
def classify(board_id):
    topics = Topic.findAll(board_id=board_id)
    topics.reverse()
    boards = Board.all()
    current_time = int(time.time())
    return render_template('topic/classify.html',
                           topics=topics,
                           boards=boards,
                           current_time=current_time)
