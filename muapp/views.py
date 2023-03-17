from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .api import get_loc_data, get_time, get_weather_data, get_icon
from .models import clothes
import sqlite3
import requests
import datetime
import math, json, sqlite3
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

# def 404(request):
#     return render(request,"404.html")

def index(request):
    location = get_loc_data()
    date = get_time()
    weather = get_weather_data()
    icon = get_icon()
    results= {
        'location' : location,
        'date' : date,
        'minTmp' : weather['minTmp'],
        'maxTmp' : weather['maxTmp'] ,
        'alertRain' : weather['alertRain'] ,
        'curTmp' : weather['curTmp'] ,
        'humidity' : weather['humidity'] ,
        'sky' : weather['sky'] ,
        'icon' : icon,
        }
    return render(request,"index.html",results)

@login_required(login_url='login')
def blog(request, username):
    user = User.objects.get(username=username)
    return render(request,"blog.html",{"user":user})

def feature(request):
    return render(request,"feature.html")

@login_required(login_url='login')
def product(request, username):
    user = User.objects.get(username=username)
    return render(request,"product.html",{"user":user})

def about(request):
    return render(request,"about.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

def logins(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method =='POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            #검증 완료시 로그인
            login(request, form.get_user())
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login2.html', {'form': form}) 


# def 데이터받아오는페이지(request):
#     clotheslist = clothes.objects.all()

#     info = {
#         'clotheslist' : clotheslist
#         }

#     return render(request,"uploadcloset.html",info )

@login_required(login_url='login')
def upload_closet(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        if request.FILES.get('imgfile'):
            new_clothes=clothes.objects.create(
                season=request.POST.get('season'),
                type1=request.POST.get('type1'),
                type2=request.POST.get('type2'),
                tag=request.POST.get('tag'),
                name=request.POST.get('name'),
                imgfile=request.FILES.get('imgfile'),
                details=request.POST.get('details'),
            )
        else:
            new_clothes=clothes.objects.create(
                season=request.POST.get('season'),
                type1=request.POST.get('type1'),
                type2=request.POST.get('type2'),
                tag=request.POST.get('tag'),
                name=request.POST.get('name'),
                imgfile=request.FILES.get('imgfile'),
                details=request.POST.get('details'),
            )
        messages.success(request,'성공적으로 등록되었습니다! ')
        return redirect('index') #상품목록으로 돌아가야함
    return render(request, 'upload_closet.html',{"user":user})


#게시글이 생성되면 index로 생성되지 않으면 글쓰기 게시판으로 돌아간다는데
# https://wikidocs.net/91438

# def remove_clothes(request, pk):
#     clothes = clothes.objects.get(pk=pk) #models.py 의 clothes
#     if request.method == 'POST':
#         post.delete()
#         return redirect('/index/') #상품목록으로 돌아가야함
#     return render(request, 'main/remove_post.html', {'clothes': clothes})