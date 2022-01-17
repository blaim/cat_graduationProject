from django.urls import path
from . import main_page

urlpatterns = [
    path('', main_page.view),
]