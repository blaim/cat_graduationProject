from django.shortcuts import render

def view(request):
    return render(request, 'main/main_page.html')