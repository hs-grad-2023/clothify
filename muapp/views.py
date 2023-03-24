from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .api import get_loc_data, get_time, get_weather_data, get_icon
from .getDB import get_clothes_list
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
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

# Create your views here.

# def 404(request):
#     return render(request,"404.html")

def index(request):
    try:
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
    except:
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
            'errcode' : 1
            }
        return render(request,"index.html",results)

@login_required(login_url='login')
def detail_closet(request, username):
    user = User.objects.get(first_name=username)
    # db = get_clothes_list()
    c = clothes.objects.all()   #clothes의 모든 객체를 c에 담기
    
    o = {
        'c' : c,
        "user":user,
    }
    return render(request,"detail_closet.html",o)

def feature(request):
    return render(request,"feature.html")

# @login_required(login_url='login')
# def product(request, username):
#     user = User.objects.get(username=username)
#     return render(request,"product.html",{"user":user})

@login_required(login_url='login')
def view_closet(request, username):
    # db = get_clothes_list()
    user = User.objects.get(first_name=username)
    c = clothes.objects.all()   #clothes의 모든 객체를 c에 담기
    
    o = {
        'c' : c,
        "user":user
    }
    
    return render(request,"view_closet.html", o)


def about(request):
    return render(request,"about.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = get_random_string(length=16)
            user.save()
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
            user = form.get_user().first_name
            if 'next' in request.POST:
                next_string = request.POST.get('next')
                result = next_string.split('/')[1]
                return redirect(f'/{result}/{user}')
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login2.html', {'form': form}) 


# @login_required(login_url='login')
# def uploadCloset(request, username):
#     error = False
#     user = User.objects.get(first_name=username)
#     if request.method == 'POST':
#         if request.FILES.get('imgfile'):
#             new_clothes=clothes.objects.create(
#                 type1=request.POST.get('type1'),
#                 type2=request.POST.get('type2'),
#                 tag=request.POST.get('tags'),
#                 name=request.POST.get('clothesName'),
#                 imgfile=request.FILES.get('imgfile'),
#                 details=request.POST.get('details'),
#             )
#             return render(request, 'upload_closet.html',{"user":user})
#         else:
#             error = True
#             print(request.FILES.get('imgfile'))
#             # messages.add_message(self.request, messages.INFO, '이미지가 없습니다.')
#     return render(request, 'upload_closet.html',{"user":user, 'error':error})
#         # return redirect('index') #상품목록으로 돌아가야함

@login_required(login_url='login')
def uploadCloset(request, username):
    user = User.objects.get(first_name=username)
    if request.method == 'POST':
        if request.FILES.get('imgfile'):
            new_clothes=clothes.objects.create(
                type1=request.POST.get('type1'),
                type2=request.POST.get('type2'),
                tag=request.POST.get('tags'),
                name=request.POST.get('clothesName'),
                imgfile=request.FILES.get('imgfile'),
                details=request.POST.get('details'),
            )
        else:
            new_clothes=clothes.objects.create(
                type1=request.POST.get('type1'),
                type2=request.POST.get('type2'),
                tag=request.POST.get('tags'),
                name=request.POST.get('clothesName'),
                imgfile=request.FILES.get('imgfile'),
                details=request.POST.get('details'),
            )
        return redirect('index') #상품목록으로 돌아가야함
    return render(request, 'upload_closet.html',{"user":user})



@login_required(login_url='login')
def blog(request, username):
    user = User.objects.get(first_name=username)
    return render(request,"blog.html",{"user":user})

@login_required(login_url='login')
def virtual_fit(request, username):
    user = User.objects.get(first_name=username)
    return render(request,"virtual_fit.html",{"user":user})


# def remove_clothes(request, pk):
#     clothes = clothes.objects.get(pk=pk) #models.py 의 clothes
#     if request.method == 'POST':
#         post.delete()
#         return redirect('/index/') #상품목록으로 돌아가야함
#     return render(request, 'main/remove_post.html', {'clothes': clothes})

def uppyTest(request):
    return render(request,"Uppy_test.html",)