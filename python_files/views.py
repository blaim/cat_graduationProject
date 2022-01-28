from django.shortcuts import render
from django.http import JsonResponse
import requests
import pprint
import json
import jwt
from python_files.tokenTest import SECRET_KEY, ALGORITHM

# Create your views here.

def home(request):
    res = render(request, 'home.html')
    token = request.COOKIES.get('token')
    print(type(token))
    if (token):
        print(token)
        access_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return render(request, 'home.html', {'nickname':'김경태'})
    return render(request, 'home.html')

def top(request):
    code = request.GET['code']
    grant_type = 'authorization_code'
    client_id = '10ecf0439a675841802b2143335b994e'
    redirect_uri = 'http://127.0.0.1:8000/top'
    # Get access_token!
    param = {
        'grant_type': grant_type,
        'client_id': client_id,
        'redirect_uri' : redirect_uri,
        'code' : code,
    }
    url = 'https://kauth.kakao.com/oauth/token'
    r = requests.post(url, data=param)
    json_result = r.json()
    access_token = json_result['access_token']
    u = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})
    user_info_result = u.json()
    nickname = user_info_result['kakao_account']['profile']['nickname']
    # 여기에서, 회원 번호를 써서 사용자 번호를 얻으면서 액세스 토큰 저장
    #data = {'user_id': 1}  # 추후에 수정 예정 - db에서 해당하는 사용자의 사용자 번호를 넣을 예정
    # 일단은 액세스 토큰을 직접 넣음.
    data = {'access_token' : access_token}
    token = jwt.encode(data, SECRET_KEY, ALGORITHM) #jwt 토큰 획득
    res = render(request, 'main/top.html', {'access_token':access_token, 'nickname':nickname})
    res.set_cookie('token', token) #만든 토큰을 쿠키에 추가
    return res


def draw(request):
    return render(request, 'main/draw_room.html')

def bootstrap(request):
    return render(request, 'main/bootstrap_test.html')

def bootstrap2(request):
    return render(request, 'main/bootstrap_test2.html')
