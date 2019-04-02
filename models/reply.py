# from model import Model
from models import Model
from utils1 import encryption
from utils1 import log
from utils1 import salt

from models.board import Board
from models.user import User


import time
from models.mongua import Mongua


class Reply(Model):
    def __init__(self, form):
        self.id = form.get('id', -1)
        self.replyer_id = int(form.get('replyer_id', -1))
        self.author_id = int(form.get('author_id', -1))
        self.topic_id = int(form.get('topic_id', -1))
        self.reply_content = form.get('reply_content', '')
        self.created_time = int(form.get('created_time', int(time.time())))
        self.updated_time = self.created_time

    def replyer_name(self):
        replyer =  User.getByid(self.replyer_id)
        return replyer

    def topic_name(self):
        topic_id = self.topic_id
        from models.topic import Topic
        topic = Topic.getByid(topic_id)
        return topic


class Reply(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('replyer_id', int, -1),
        ('author_id', int, -1),
        ('topic_id', int, -1),
        ('reply_content', str, ''),
        ('topic_content', str, ''),
        ('created_time', int, int(time.time())),
        ('updated_time', int, int(time.time())),
    ]
    #
    # def __init__(self, form):
    #     self.id = form.get('id', -1)
    #     self.replyer_id = int(form.get('replyer_id', -1))
    #     self.author_id = int(form.get('author_id', -1))
    #     self.topic_id = int(form.get('topic_id', -1))
    #     self.reply_content = form.get('reply_content', '')
    #     self.created_time = int(form.get('created_time', int(time.time())))
    #     self.updated_time = self.created_time

    def replyer_name(self):
        replyer =  User.getByid(self.replyer_id)
        return replyer

    def topic_name(self):
        topic_id = self.topic_id
        from models.topic import Topic
        topic = Topic.getByid(topic_id)
        return topic

