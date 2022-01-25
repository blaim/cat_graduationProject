from django.shortcuts import render
import requests
import pprint
import json

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
    print(r.json())
    access_token = json_result['access_token']
    u = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})
    user_info_result = u.json()
    nickname = user_info_result['kakao_account']['profile']['nickname']
    print(nickname)
    return render(request, 'main/top.html', {'access_token':access_token, 'nickname':nickname})

def draw(request):
    return render(request, 'main/draw_room.html')

def bootstrap(request):
    return render(request, 'main/bootstrap_test.html')

def bootstrap2(request):
    return render(request, 'main/bootstrap_test2.html')
