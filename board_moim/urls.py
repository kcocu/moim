
from django.urls import path
from . import views



app_name = 'board_moim'

urlpatterns = [
    path('', views.board_moim, name='board_moim'),
    path('list/', views.list_moim, name='list_moim'),
    path('<int:pk>/', views.board_detail, name='board_detail'),
    path('update/<int:pk>/', views.board_update, name='board_update'),
    path('delete/<int:pk>/', views.board_delete, name='board_detele'),
    path('comment/', views.comment, name='board_comment'),
    path('list/search/', views.search, name='search'),
    path('<int:pk>/kick/', views.kick, name='kick'),
]