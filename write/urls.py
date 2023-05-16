from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views



app_name = 'write'

urlpatterns = [
    path('free/<int:free_id>/', views.free, name='free'),
    # path('join/', views.join, name='join'),
    
    path('join/<int:make_id>/', views.join_detail, name='join_detail'),
    path('join/<int:make_id>/comment/', views.join_comment, name='join_comment'),

    path('join/<int:make_id>/comment/update/', views.join_comment_u, name='join_comment_u'),
    path('join/<int:make_id>/comment/delete/', views.join_comment_d, name='join_comment_d'),

    path('join/join_write/', views.join, name='join_write'),
    path('gallery/<int:pk>/', views.gallery, name='gallery'),
    path('gallery/<int:pk>/<int:gg>/', views.gallery_single, name='gallery_single'),
    
    path('gallery/<int:pk>/<int:gg>/delete/', views.gallery_delete, name='gallery_delete'),
    path('gallery/<int:pk>/<int:gg>/modify/', views.gallery_modify, name='gallery_modify'),
    path('gallery/<int:pk>/<int:gg>/modify2/', views.gallery_modify2, name='gallery_modify2'),
    path('gallery/<int:pk>/<int:gg>/modify2/delete/', views.gallery_img_delete, name='gallery_img_delete' ),
    path('gallery/<int:pk>/<int:gg>/modify3/', views.gallery_modify3, name='gallery_modify3' ),
    path('download/', views.download, name='download' ),

    path('new_face/', views.new_face, name='new_face'),
    path('gallery/<int:pk>/gallery_makeit/', views.gallery_makeit, name='gallery_makeit'),
    path('', views.board_list, name='board_list'),
    # path('borad_left/', views.borad_left, name='borad_left'),
    path('free/<int:free_id>/free_write/', views.board_free_write, name='free_write'),
    path('<int:pk>/comments/', views.comments_create, name='comments_create'),

    path('join/<int:make_id>/delete/', views.join_delete, name='join_delete' ),
    path('join/<int:make_id>/modify/', views.join_modify, name='join_modify' ),
    path('join/<int:make_id>/modify2/', views.join_modify2, name='join_modify2' ),


    # path('gallery/<int:pk>/', views.gallery_detail, name='gallery_detail'),
    path('comments/<int:free_id>/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    # path('<int:free_pk>/likes/', views.likes, name='likes'),
    path('freeboard_index/<int:free_id>/', views.freeboard_index, name='freeindex'),#자유게인덱스
    path('viewtext/<int:free_id>/<int:pk>/', views.view_text, name='free01' ),#view text, vt 게시물보기
    path('viewtext/<int:free_id>/<int:pk>/delete/', views.text_delete, name='delete' ),
    path('viewtext/<int:free_id>/<int:pk>/modify/', views.text_modify, name='modify' ),

    path('free/<int:pk>/search/', views.free_search, name='free_search'),#검색
    path('gallery/<int:pk>/search/', views.gallery_search, name='gallery_search'),#검색
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)