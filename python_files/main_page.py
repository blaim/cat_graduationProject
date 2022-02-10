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
    if token!='None' and token != None:
        tokenAlive='True'
        id = ObjectId(jwt.decode(token, SECRET_KEY, ALGORITHM)['id'])
        access_token = userChecker.checkToken(id)
        nickname = userChecker.checkNickname(id)
        if (access_token!=None):
            a = requests.get('https://kapi.kakao.com/v1/user/access_token_info', headers={"Authorization": f'Bearer ${access_token}'})
            if a.json().get('id') == None:# 토큰이 죽어있다면 None을 반환한다.
                if a.json()['code']==-401: #토큰이 만료되었다면 토큰을 없는 것으로 처리한다.
                    token = None
                    tokenAlive='False'
        else :
            tokenAlive='False'
    if token=='None' or token == None:
        tokenAlive='False'
    # render 함수에서 세 번째 인자가 context이고, 그걸로 token의 활성화 여부를 보낸다.
    # 만약 토큰이 죽어 있다면 로그인 버튼을 띄우고, 아니면 로그인 버튼을 비활성화한다.
    res = render(request, 'main/main_page.html', {'nickname': nickname, 'tokenAlive': tokenAlive})
    res.set_cookie('token',token)
    return res