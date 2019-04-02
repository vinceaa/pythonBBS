from flask import Flask

from test_routes.index import main as index
from test_routes.user import main as user
from test_routes.board import main as board
from test_routes.topic import main as topic
from test_routes.reply import main as reply

app = Flask(__name__)

import config


app.register_blueprint(index)
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(board, url_prefix='/board')
app.register_blueprint(topic, url_prefix='/topic')
app.register_blueprint(reply, url_prefix='/reply')

app.secret_key = config.secret_key


def __main():
    config = dict(
        host='0.0.0.0',
        port=2000,
        debug=True,
    )
    app.run(**config)


__main()
