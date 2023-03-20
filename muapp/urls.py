"""muproject URL Configuration

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
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from muapp import views
# index는 대문, blog는 게시판
# from main.views import index, blog, posting

# 이미지를 업로드하자
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    # path('404', views.404, name='404'),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('about/',views.about, name='about'),
    path('blog/<str:username>/',views.blog, name='blog'),
    path('feature/',views.feature, name='feature'),
    # path('product/<str:username>/', views.product, name='product'),
    path('login/', views.logins, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('upload_closet/<str:username>/',views.upload_closet, name='upload_closet'),
    path('upload_files',views.upload_file,name='upload_file'),
    path('view_closet/<str:username>/',views.view_closet, name='view_closet'),
    path('detail_closet/<str:username>/',views.detail_closet, name='detail_closet'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)