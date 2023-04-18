from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib import messages
# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home");
    if request.method == "GET":
        return render(request,'login/login.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.add_message(request, messages.ERROR,
                                 'Wrong Password', "alert-danger")
            return redirect("login:login");
        auth_login(request,user)
        return redirect("dashboard:home");
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect("login:login")
    else:
        return redirect("login:login")