from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session,
)

from models.user import User

main = Blueprint('board', __name__)

from utils1 import encryption
from utils1 import log
from utils1 import salt

from models.board import Board



def current_user():
    username = session.get('username', '[游客]')
    return username


@main.route('/')
def index():
    username = current_user()
    boards = Board.all()
    return render_template('board/index.html',
                           username=username,
                           boards=boards)


@main.route('/new')
def new():
    return render_template('board/new.html')


@main.route('/add', methods=['post'])
def add():
    form = request.form
    Board.new(form)
    return redirect(url_for('.index'))


@main.route('/edit/<int:board_id>')
def edit(board_id):
    return render_template('board/edit.html', board_id=board_id)


@main.route('/update/<int:board_id>', methods=['post'])
def update(board_id):
    form = request.form
    update_name = form['board_name']
    Board.update(board_id, board_name=update_name)
    return redirect(url_for('.index'))


@main.route('/delete/<int:board_id>')
def delete(board_id):
    Board.deleteById(board_id)
    return redirect(url_for('.index'))

