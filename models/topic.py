# from model import Model
from models import Model
from utils1 import encryption
from utils1 import log
from utils1 import salt
# from utils1 import time_flow

from models.board import Board
from models.reply import Reply
from models.user import User

import time
from models.mongua import Mongua
import json


class Topic(Model):
    def __init__(self, form):
        # print('** form:', form)
        self.id = form.get('id', -1)
        self.user_id = int(form.get('user_id', -1))
        self.board_id = int(form.get('board_id', -1))
        self.topic_title = form.get('topic_title', '')
        self.topic_content = form.get('topic_content', '')
        self.created_time = int(form.get('created_time', int(time.time())))
        self.updated_time = self.created_time
        self.views_number = int(form.get('views_number', 0))

    def board(self):
        board_id = self.board_id
        ins = Board.getByid(board_id)
        return ins.board_name

    def replys(self):
        topic_id = self.id
        replys = Reply.findAll(topic_id=topic_id)
        return replys

    def reply_number(self):
        return len(self.replys())

    def topic_author(self):
        replyer =  User.getByid(self.user_id)
        return replyer
#
#
# class Cache(object):
#     def get(self, key):
#         pass
#
#     def set(self, key, value):
#         pass
#
#
# class RedisCache(Cache):
#     import redis
#     redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)
#
#     def set(self, key, value):
#         return RedisCache.redis_db.set(key, value)
#
#     def get(self, key):
#         return RedisCache.redis_db.get(key)


# mongo 版本
class Topic(Mongua):

    __fields__ = Mongua.__fields__ + [
        ('content', str, ''),
        ('user_id', int, -1),
        ('board_id', int, -1),
        ('topic_title', str, ''),
        ('topic_content', str, ''),
        ('created_time', int, int(time.time())),
        ('updated_time', int, int(time.time())),
        ('views_number', int, 0),
    ]


    should_update_all = True


    # def __init__(self, form):
    #     # print('** form:', form)
    #     self.id = form.get('id', -1)
    #     self.user_id = int(form.get('user_id', -1))
    #     self.board_id = int(form.get('board_id', -1))
    #     self.topic_title = form.get('topic_title', '')
    #     self.topic_content = form.get('topic_content', '')
    #     self.created_time = int(form.get('created_time', int(time.time())))
    #     self.updated_time = self.created_time
    #     self.views_number = int(form.get('views_number', 0))

    def board(self):
        board_id = self.board_id
        ins = Board.getByid(board_id)
        if ins is None:
            return ''
        else:
            return ins.board_name

    def replys(self):
        topic_id = self.id
        replys = Reply.findAll(topic_id=topic_id)
        return replys

    def reply_number(self):
        return len(self.replys())

    def topic_author(self):
        replyer =  User.getByid(self.user_id)
        return replyer









