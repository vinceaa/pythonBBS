import time
from pymongo import MongoClient
from utils1 import encryption
from utils1 import salt
import json

mongua = MongoClient()
# redis 版本

def timestamp():
    return int(time.time())


def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    # 存储数据的 id
    doc = mongua.db['data_id']
    # find_and_modify 是一个原子操作函数
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id


class Cache(object):
    def get(self, key):
        pass

    def set(self, key, value):
        pass


class RedisCache(Cache):
    import redis
    redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set(self, key, value):
        return RedisCache.redis_db.set(key, value)

    def get(self, key):
        return RedisCache.redis_db.get(key)


class Mongua(object):
    __fields__ = [
        '_id',
        # (字段名, 类型, 值)
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
    ]

    # 定义 redis
    should_update_all = True
    redis_cache = RedisCache()

    # @classmethod
    def to_json(self):
        d = dict()
        for k in self.__fields__:
            key = k[0]
            if not key.startswith('_'):
                # print('keys;', key)
                # print('self.dict:', self.__dict__)
                d[key] = getattr(self,key)
        return json.dumps(d)

    @classmethod
    def from_json(cls, j):
        d = json.loads(j)

        instance = cls()
        for k, v in d.items():
            setattr(instance, k, v)
        return instance

    @classmethod
    def all_delay(self):
        time.sleep(3)
        return self.all()

    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.save()
        return m

    # def save(self):
    #     super(Topic, self).save()
    #     should_update_all = True


    @classmethod
    def cache_all(cls):
        print('redis cache')
        if cls.should_update_all:
            print('更新')
            cls.redis_cache.set('topic_all', json.dumps([i.to_json() for i in cls.all_delay()]))
            cls.should_update_all = False
        j = json.loads(cls.redis_cache.get('topic_all').decode('utf-8'))
        j = [cls.from_json(i) for i in j]
        return j



    @classmethod
    def has(cls, **kwargs):
        """
        检查一个元素是否在数据库中 用法如下
        User.has(id=1)
        :param kwargs:
        :return:
        """
        return cls.find_one(**kwargs) is not None

    def mongos(self, name):
        return mongua.db[name]._find()

    def __repr__(self):
        form = self.__dict__.items()
        classname = self.__class__.__name__
        forms = '<\n' + '\n'.join(['{} = {}'.format(k, v) for k, v in form]) + '\n> \n'
        new_form = '{}{}'.format(classname, forms)
        return new_form

    @classmethod
    def new(cls, form=None, **kwargs):
        """
        new 是给外部使用的函数
        """
        name = cls.__name__
        m = cls()
        # 把定义的数据写入空对象, 未定义的数据输出错误
        fields = cls.__fields__.copy()
        # 去掉 _id 这个特殊的字段
        fields.remove('_id')
        if form is None:
            form = {}

        for f in fields:
            k, t, v = f
            if k in form:
                if k == 'password':
                    setattr(m, k, t(encryption(salt, form[k])))
                else:
                    setattr(m, k, t(form[k]))
            else:
                # 设置默认值
                setattr(m, k, v)
        # 处理额外的参数 kwargs
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        # 写入默认数据
        m.id = next_id(name)
        # print('debug new id ', m.id)
        ts = int(time.time())
        m.created_time = ts
        m.updated_time = ts
        # m.deleted = False
        m.type = name.lower()
        # 特殊 model 的自定义设置
        # m._setup(form)
        m.save()
        return m

    #
    # @classmethod
    # def new(cls, form, **kwargs):
    #     ins = cls(form)
    #     #  给原始密码加密
    #     if hasattr(ins, 'password'):
    #         print('有 passowrd 属性')
    #         ins.password = encryption(salt, ins.password)
    #     for k, v in kwargs.items():
    #         setattr(ins, k, v)
    #     ins.save()
    #     return ins
    #
    #

    @classmethod
    def _new_with_bson(cls, bson):
        """
        这是给内部 all 这种函数使用的函数
        从 mongo 数据中恢复一个 model
        """
        m = cls()
        fields = cls.__fields__.copy()
        # 去掉 _id 这个特殊的字段
        # fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                # 设置默认值
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        # 这一句必不可少，否则 bson 生成一个新的_id
        # FIXME, 因为现在的数据库里面未必有 type
        # 所以在这里强行加上
        # 以后洗掉db的数据后应该删掉这一句
        m.type = cls.__name__.lower()
        return m

    @classmethod
    def all(cls):
        # 按照 id 升序排序
        # name = cls.__name__
        # ds = mongua.db[name].find()
        # l = [cls._new_with_bson(d) for d in ds]
        # return l
        return cls._find()

    # TODO, 还应该有一个函数 find(name, **kwargs)
    @classmethod
    def _find(cls, **kwargs):
        """
        mongo 数据查询
        """
        name = cls.__name__
        # TODO 过滤掉被删除的元素
        # kwargs['deleted'] = False
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = mongua.db[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]
        # print('l: ', l)
        return l

    @classmethod
    def _find_raw(cls, **kwargs):
        name = cls.__name__
        ds = mongua.db[name]._find(kwargs)
        l = [d for d in ds]
        return l
        # 直接 list() 就好了
        # return list(l)

    @classmethod
    def _clean_field(cls, source, target):
        """
        清洗数据用的函数
        例如 User._clean_field('is_hidden', 'deleted')
        把 is_hidden 字段全部复制为 deleted 字段
        """
        ms = cls._find()
        for m in ms:
            v = getattr(m, source)
            setattr(m, target, v)
            m.save()

    @classmethod
    def findBy(cls, **kwargs):
        # print('** findBy 进行', kwargs.items())
        # print('** find one 结果:', cls.find_one(**kwargs))
        return cls.find_one(**kwargs)

    @classmethod
    def findAll(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def getByid(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def find_one(cls, **kwargs):
        """
        """
        # TODO 过滤掉被删除的元素
        # kwargs['deleted'] = False
        l = cls._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None

    # @classmethod
    # def upsert(cls, query_form, update_form, hard=False):
    #     ms = cls.find_one(**query_form)
    #     if ms is None:
    #         query_form.update(**update_form)
    #         ms = cls.new(query_form)
    #     else:
    #         ms.update(update_form, hard=hard)
    #     return ms
    #
    # def update(self, form, hard=False):
    #     for k, v in form.items():
    #         if hard or hasattr(self, k):
    #             setattr(self, k, v)
    #     # self.updated_time = int(time.time()) fixme
    #     self.save()

    #  update 原始函数
    # @classmethod
    # def update(cls, i, **kwargs):
    #     id = i
    #     ins = cls.getByid(id)
    #     if ins != []:
    #         update_ins = ins.__dict__
    #         # print('update_ins:', update_ins)
    #         data = cls.all_data()
    #         # print('data:', data)
    #         for key, value in kwargs.items():
    #             k, v = key, value
    #         for e in data:
    #             print('e, update_ins, tf:', e, update_ins, e == update_ins)
    #             if e == update_ins:
    #                 print('good')
    #                 e[k] = v
    #                 path = cls.path()
    #                 save(path, data)
    #                 return e
    #     else:
    #         return []

    #  mongo 版的 update 函数
    @classmethod
    def update(cls, i, **kwargs):
        id = i
        ins = cls.getByid(id)
        if ins != []:
            # update_ins = ins.__dict__

            for key, value in kwargs.items():
                k, v = key, value
            setattr(ins, k, v)
            name = ins.__class__.__name__
            # save 变的简单了，直接 save ins.__dict__ 即可
            mongua.db[name].save(ins.__dict__)
            cls.should_update_all = True

            # print('update_ins:', update_ins)
            # data = cls.all_data()
            # # print('data:', data)
            # for key, value in kwargs.items():
            #     k, v = key, value
            # for e in data:
            #     print('e, update_ins, tf:', e, update_ins, e == update_ins)
            #     if e == update_ins:
            #         print('good')
            #         e[k] = v
            #         path = cls.path()
            #         save(path, data)
            #         return e
        else:
            return []


    #     todo
    @classmethod
    def deleteById(cls, id):
        name = cls.__name__
        query = {
            'id': id,
        }
        values = {
            'deleted': True
        }
        mongua.db[name].update_one(query, values)
        cls.should_update_all = True


        # self.deleted = True
        # self.save()


    def save(self):
        name = self.__class__.__name__
        mongua.db[name].save(self.__dict__)
        self.__class__.should_update_all = True
        # self.should_update_all = True

    #  mongo 版的 delete ，还没试
    # def delete(self):
    #     name = self.__class__.__name__
    #     query = {
    #         'id': self.id,
    #     }
    #     values = {
    #         'deleted': True
    #     }
    #     mongua.db[name].update_one(query, values)
    #     # self.deleted = True
    #     # self.save()

    @classmethod
    def userId(cls, username):
        ins = cls.findBy(username=username)
        if ins is None:
            return -1
        else:
            # print('ins', ins)
            return ins.id


    def blacklist(self):
        b = [
            '_id',
        ]
        return b

    def json(self):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        # TODO, 增加一个 type 属性
        return d

    def data_count(self, cls):
        """
        神奇的函数, 查看用户发表的评论数
        u.data_count(Comment)

        :return: int
        """
        name = cls.__name__
        # TODO, 这里应该用 type 替代
        fk = '{}_id'.format(self.__class__.__name__.lower())
        query = {
            fk: self.id,
        }
        count = mongua.db[name]._find(query).count()
        return count

    def time_flow(self, start, now):
        interval = int(now - start)
        minute_flow = int(interval / 60)

        if interval < 60:
            flow_str = '{} 秒前'.format(interval)
        elif interval in range(60, 3600):
            flow = int(interval / 60)
            flow_str = '{} 分钟前'.format(flow)
        elif interval in range(3600, 86400):
            flow = int(interval / 3600)
            flow_str = '{} 小时前'.format(flow)
        elif interval in range(86400, 2592000):
            flow = int(interval / 86400)
            flow_str = '{} 天前'.format(flow)
        elif interval in range(2592000, 31104000):
            flow = int(interval / 2592000)
            flow_str = '{} 月前'.format(flow)
        else:
            flow = int(interval / 31104000)
            flow_str = '{} 年前'.format(flow)
        return flow_str

    def change_time(self, times):
        format = '%Y/%m/%d %H:%M:%S'
        value = time.localtime(times)
        dt = time.strftime(format, value)
        return dt

