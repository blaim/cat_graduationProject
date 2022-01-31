from django.shortcuts import render
import requests
import jwt
from bson.objectid import ObjectId
from python_files.tokenTest import SECRET_KEY, ALGORITHM
from python_files.user_check import userChecker
# Create your views here.
def view(request):
    nickname = '없음'
    token = request.COOKIES.get('token') #token은 액세스 키를 가지고 jwt 인코딩으로 만든 값이다. 자세한 건 python_files/views.py 확인
    access_token=None
    print(token)
    if (token!=None):
        id = ObjectId(jwt.decode(token, SECRET_KEY, ALGORITHM)['id'])
        access_token = userChecker.checkToken(id)
        nickname = userChecker.checkNickname(id)
        if (access_token!=None):
            a = requests.get('https://kapi.kakao.com/v1/user/access_token_info', headers={"Authorization": f'Bearer ${access_token}'})
            if a==-401: #토큰이 만료되었다면 토큰을 없는 것으로 처리한다.
                token = None
    res = render(request, 'main/main_page.html', {'nickname': nickname})
    res.set_cookie('token',token)
    return res