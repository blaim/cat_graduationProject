from pymongo import MongoClient
from bson.objectid import ObjectId
class userInformation:

    def __init__(self):
        self.host = "localhost"
        self.port = "27017"
        self.connection = MongoClient(self.host, int(self.port))
        self.db=self.connection['userInfo']
        self.udb=self.db['users']
        if self.udb == None:
            self.udb.insert_one({'userId':'none'})

    def checkUserDB(self, userID):
        if self.udb.find_one({'userId':userID})==None:
            return False
        else:
            return True

    def addUser(self, userID, nickname):
        self.udb.insert_one({'userId':userID, 'nickname':nickname, 'accessToken':'none'})

    def checkToken(self, id):
        info = self.udb.find_one({'_id':id})
        if info != None:
            info = info['accessToken']
        return info

    def setToken(self, id, token):
        self.udb.update_one({'_id':id},{"$set":{'accessToken':token}}, upsert=True)

    def checkNickname(self, id):
        info = self.udb.find_one({'_id':id})
        if info != None:
            info = info['nickname']
        return info

    def checkID(self, userID):
        info = self.udb.find_one({'userId':userID})
        if info != None:
            info=info['_id']
        # _id는 ObjectID 타입이므로 문자열로 변환하여 반환한다.
        return str(info)

userChecker = userInformation()
# 1. 토큰 정보로 회원번호 확인
# 2. 회원번호로, 회원 정보가 있는지 확인
# 3. 회원 정보가 없다면 db에 추가
# 4. db 기준으로, 회원의 인덱스 번호를 반환

