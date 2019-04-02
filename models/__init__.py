import json

from utils1 import encryption
from utils1 import salt

import time

def loads(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def save(path, data):
    data = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        return f.write(data)


class Model(object):

    # 载入所有的数据
    @classmethod
    def all_data(cls):
        path = cls.path()
        data = loads(path)
        return data

    #  生成新的数据
    @classmethod
    def new(cls, form, **kwargs):
        ins = cls(form)
        #  给原始密码加密
        if hasattr(ins, 'password'):
            print('有 passowrd 属性')
            ins.password = encryption(salt, ins.password)
        for k, v in kwargs.items():
            setattr(ins, k, v)
        ins.save()
        return ins

    def save(self):
        attrs = self.__dict__
        path = self.path()
        data = loads(path)
        if data == []:
            self.id = 0
        else:
            self.id = data[-1]['id'] + 1
        data.append(attrs)
        save(path, data)

    @classmethod
    def path(cls):
        cls_name = cls.__name__
        path_name = 'db/{}.txt'.format(cls_name)
        return path_name

    #  载入所有的数据
    @classmethod
    def all(cls):
        path = cls.path()
        data = loads(path)
        data_ins = [cls(e) for e in data]
        return data_ins

    #  通过属性找到所有的数据
    @classmethod
    def findAll(cls, **kwargs):
        all_ins = cls.all()
        lista = []
        for key, value in kwargs.items():
            k, v = key, value
        for ins in all_ins:
            if ins.__dict__[k] == v:
                lista.append(ins)
        return lista

    #  通过属性找到第一条数据
    @classmethod
    def findBy(cls, **kwargs):
        all_ins = cls.all()
        for key, value in kwargs.items():
            k, v = key, value
        for ins in all_ins:
            # print('** 类里的 ins:', ins.__dict__[k], v, ins.__dict__[k] == v)
            if ins.__dict__[k] == v:
                return ins
        return []

    #  通过 id 查找数据
    @classmethod
    def getByid(cls, id):
        return cls.findBy(id=id)

    # 通过 id 删除一条数据
    @classmethod
    def deleteById(cls, id):
        ins = cls.getByid(id)
        if ins != []:
            delete_ins = ins.__dict__
            path = cls.path()
            data = loads(path)
            for e in data:
                if e == delete_ins:
                    data.remove(e)
                    save(path, data)
            return delete_ins
        else:
            return []

    # 通过 id 更新一条数据
    @classmethod
    def update(cls, i, **kwargs):
        id = i
        ins = cls.getByid(id)
        if ins != []:
            update_ins = ins.__dict__
            # print('update_ins:', update_ins)
            data = cls.all_data()
            # print('data:', data)
            for key, value in kwargs.items():
                k, v = key, value
            for e in data:
                print('e, update_ins, tf:', e, update_ins, e == update_ins)
                if e == update_ins:
                    print('good')
                    e[k] = v
                    path = cls.path()
                    save(path, data)
                    return e
        else:
            return []


    @classmethod
    def userId(cls, username):
        ins = cls.findBy(username=username)
        if ins == []:
            return -1
        else:
            return ins.id

    def __repr__(self):
        form = self.__dict__.items()
        classname = self.__class__.__name__
        forms = '<\n' + '\n'.join(['{} = {}'.format(k, v) for k, v in form]) + '\n> \n'
        new_form = '{}{}'.format(classname, forms)
        return new_form

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
