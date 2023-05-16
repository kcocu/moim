"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin', admin.site.urls), #admin, admin@admin.com, 1234
    path('write/', include('write.urls')),
    path('select_moim/', include('select_moim.urls')),
    path('make_moim/', include('make_moim.urls')),
    path('board_moim/', include('board_moim.urls')),
    path('profile/', include('all_info.urls')),
    path('login/', views.login,name='login'
    ),
    path('logout/', views.logout,name='logout'
    ),
    path('', views.home, name='home'
    ),
    path('search/', views.search, name='search'),#검색
    path('signup/', views.signup, name='signup'),#회원가입

    # path('loginfo/', include('loginfo.urls')),
    # path('login/',
    #     auth_views.LoginView.as_view(template_name='member/login.html'),
    #     name='login'
    # ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
