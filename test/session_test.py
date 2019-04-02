import random

session = {}

# def random_str():
#     init = 'aklhsdkahsdhashdahskdjhjkahdskjhk'
#     str = ''
#     for i in range(len(init)):
#         str += init[random.randint(0, len(init) - 1)]
#     return str
#
#
# def make_session():
#     user.cookie = random_str()
#     session[random] = username
#
#
#     for k, v in session.items():
#         if k == user.cookie:
#             return v == session['k']

import hashlib



def __main():
    hash = hashlib.sha256()
    hash.update('hahaha'.encode('utf-8'))
    print(hash.hexdigest())

__main()