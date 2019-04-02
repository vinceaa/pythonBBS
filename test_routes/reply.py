from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session,
)

from models.user import User

main = Blueprint('reply', __name__)

from utils1 import encryption
from utils1 import log
from utils1 import salt

from models.reply import Reply


@main.route('/infor', methods=['post'])
def index():
    form = request.form
    log('**form:', form)
    Reply.new(form)
    topic_id = form['topic_id']
    return redirect(url_for('topic.detail', topic_id=topic_id))
