# from model import Model
from models import Model
from utils1 import encryption
from utils1 import log
from utils1 import salt
from models.mongua import Mongua



class User(Model):
    def __init__(self, form):
        self.id = form.get('id', -1)
        self.username = str(form.get('username', ''))
        self.password = str(form.get('password', ''))
        self.avatar_path = form.get('avatar_path', '')

    def register_check(form):
        username = form['username']
        password = form['password']
        ins = User.findBy(username=username)
        if ins != []:
            return False
        else:
            return len(username) > 2 and len(password) > 2

    def login_check(form):
        username = form['username']
        password = form['password']
        ins = User.findBy(username=username)
        if ins == []:
            return False
        else:
            return ins.password == encryption(salt, password)



class User(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('avatar_path', str, ''),
    ]


    def register_check(form):
        username = form['username']
        password = form['password']
        ins = User.findBy(username=username)
        # print('是否找到：', ins)
        if ins is not None:
            return False
        else:
            return len(username) > 2 and len(password) > 2

    def login_check(form):
        username = form['username']
        password = form['password']
        ins = User.findBy(username=username)
        if ins is None:
            return False
        else:
            # print('ins.password:', ins.password)
            return ins.password == encryption(salt, password)









