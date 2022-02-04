from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib import messages

def delete(request):
    cp = request.POST.get("passcheck")
    if check_password(cp, request.user.password):
        request.user.pic.delete()
        request.user.delete()
        return redirect("acc:index")
    else: # 19일차!!!
        messages.error(request, "패스워드가 일치하지 않아 삭제되지 않았습니다!")
    return redirect("acc:profile")

def update(request):
    if request.method == "POST":
        u = request.user
        pw = request.POST.get("upass")
        co = request.POST.get("ucomm")
        pi = request.FILES.get("upic")
        if pw:
            u.set_password(pw)
        if pi:
            u.pic.delete()
            u.pic = pi
        u.comment = co
        u.save()
        login(request, u)
        return redirect("acc:profile")
    return render(request, "acc/update.html")


def profile(request):
    return render(request, "acc/profile.html")

def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        ag = request.POST.get("uage")
        co = request.POST.get("ucomm")
        pi = request.FILES.get("upic")
        try:
            User.objects.create_user(username=un, password=pw, age=ag, comment=co, pic=pi) 
            return redirect("acc:login")
        except:
            messages.info(request, "이미 존재하는 계정이름입니다!")
    return render(request, "acc/signup.html")


def index(request):
    return render(request, "acc/index.html")

def login_user(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        user = authenticate(username=un, password=pw)
        if user:
            login(request, user)
            messages.success(request, f"{request.user} 님 환영합니다!!")
            return redirect("acc:index")
        else: # 19일 차때 채워놓을 곳!
            messages.error(request, "계정정보가 일치하지 않습니다 :(")
    return render(request, "acc/login.html")

def logout_user(request):
    logout(request)
    return redirect('acc:login')

