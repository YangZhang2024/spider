from pymongo import MongoClient
client = MongoClient("localhost", 27017)
db = client.pic
scrtv = client.pic['4scrtv']
import  requests
import time




# r = scrtv.find_one(record)
# print(r)

import os
# dirs = os.listdir('E:\\data\\pictures')
# for d in dirs:
#     record = {
#         "pic_set_name": d
#     }
#     scrtv.insert_one(record)

if __name__ == '__main__':
    start = time.time()
    requests.get('https://base.jingmin.wang//passimg/mt/359092/01.jpg').text
    print(time.time()-start)

