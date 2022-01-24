from django.urls import path
from . import main_page
from . import views

urlpatterns = [
    path('', main_page.view),
    path('top/', views.top, name = 'top'),
]