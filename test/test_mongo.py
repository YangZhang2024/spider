from pymongo import MongoClient
client = MongoClient("localhost", 27017)
db = client.pic
scrtv = client.pic['4scrtv']



# r = scrtv.find_one(record)
# print(r)

import os
# dirs = os.listdir('E:\\data\\pictures')
# for d in dirs:
#     record = {
#         "pic_set_name": d
#     }
#     scrtv.insert_one(record)


