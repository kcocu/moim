from django.urls import path
from . import views



app_name = 'make_moim'

urlpatterns = [
    path('', views.make_moim, name='make_moim'),
    path('signup/', views.make_moim_signup, name='make_moim_signup'),#모임가입
]