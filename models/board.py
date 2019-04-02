# from model import Model
from models import Model
from utils1 import encryption
from utils1 import log
from utils1 import salt
from models.mongua import Mongua


class Board(Model):
    def __init__(self, form):
        self.id = form.get('id', -1)
        self.board_name = form.get('board_name', '')

class Board(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('replyer_id', id, -1),
        ('board_name', str, ''),
    ]

    # def __init__(self, form):
    #     self.id = form.get('id', -1)
    #     self.board_name = form.get('board_name', '')





