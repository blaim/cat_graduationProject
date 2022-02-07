from pymongo import MongoClient
from bson.objectid import ObjectId
class userInformation:

    def __init__(self):
        self.host = "localhost"
        self.port = "27017"
        self.connection = MongoClient(self.host, int(self.port))
        self.db=self.connection.userInfo

    def checkUserDB(self, userID):
        udb=self.db.users
        if udb.find_one({'userId':userID})==None:
            return False
        else:
            return True

    def addUser(self, userID, nickname):
        udb=self.db.users
        udb.insert_one({'userId':userID, 'nickname':nickname})

    def checkToken(self, id):
        udb=self.db.users
        return udb.find_one({'_id':id})['accessToken']

    def setToken(self, id, token):
        udb=self.db.users
        udb.update_one({'_id':id},{"$set":{'accessToken':token}}, upsert=True)

    def checkNickname(self, id):
        udb=self.db.users
        return udb.find_one({'_id':id})['nickname']

    def checkID(self, userID):
        udb=self.db.users
        id=udb.find_one({'userId':userID})['_id']
        # _id는 ObjectID 타입이므로 문자열로 변환하여 반환한다.
        return str(id)

userChecker = userInformation()
# 1. 토큰 정보로 회원번호 확인
# 2. 회원번호로, 회원 정보가 있는지 확인
# 3. 회원 정보가 없다면 db에 추가
# 4. db 기준으로, 회원의 인덱스 번호를 반환

