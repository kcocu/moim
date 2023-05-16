from django.urls import path
from . import views

app_name = 'all_info'

urlpatterns = [
    path('<str:id>/', views.detail, name='profile_detail'),
    path('', views.profile_view, name='profile_view'),
    path('update/<str:id>/', views.update, name='profile_update'),#프로필 수정시 여기 클릭
    path('delete/<str:id>/', views.delete, name='profile_delete'),
    # path('update', views.profile_update_view, name='profile_update_view'),

]