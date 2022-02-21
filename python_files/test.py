import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.Room
room = db.OneRoom
import json
j = 0
fd = room.find({}, {'_id': 0 , 'URL':1, '월세': 1, '주소': 1})
dict = {}
dict = list(dict.items())
print(dict)
with open('../static/json/data.json', 'w', encoding='utf-8-sig')as f:
    for i in fd:
        dict.insert(j,i)
        print(dict[j])
        j += 1
    json.dump(dict, f,  ensure_ascii = False,indent=3)
#with open('./data.json', 'w') as f:
    #json.dump(i, f,ensure_ascii=False,indent=2)
