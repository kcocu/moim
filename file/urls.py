from django.urls import path
from . import views
app_name = 'file'
urlpatterns = [
path('upload/', views.upload, name='upload'),
path('upload_f/', views.upload_f, name='upload_f'),
]