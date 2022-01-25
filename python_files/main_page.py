from django.shortcuts import render
import jwt
# Create your views here.
def view(request):
    res = render(request, 'main/main_page.html')
    token = request.COOKIES.get('token') #token은 액세스 키를 가지고 jwt 인코딩으로 만든 값이다. 자세한 건 python_files/views.py 확인
    print(type(token))
    if (token):
        print(token)
        return render(request, 'main/main_page.html', {'nickname': '김경태'})
    return res