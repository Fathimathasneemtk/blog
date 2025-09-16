from .models import Profile
import re
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
 
# Create your views here.
 
def user_register(request):
    if request.method=="POST":
        data=request.POST
        username=data.get("username")
        first_name=data.get("first_name")
        last_name=data.get("last_name")
        password=data.get("password")
        contact_no=data.get("contact_no")
        email=data.get("email")
        type=data.get("type")
        profile_pic=request.FILES.get("profile_pic")
        if User.objects.filter(email=email):
            messages.error(request,"User with this email already exits")
        elif User.objects.filter(username=username):
            messages.error(request,"User with this username already exists")
        elif len(password)<8 or not bool(re.search(r'[^a-zA-Z0-9]', password)):
            messages.error(request,"Password should contain at least 8 char,minimum of a specail char,a capital and a small letter.")
        user=User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email)
        user.set_password(password)
        user.save()
        profile=Profile.objects.create(user=user,contact_no=contact_no,profile_pic=profile_pic,type=type)
        messages.info(request,"User created successfully.")
        return redirect("login")
    return render(request,"register.html")
 
 
 
def user_login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(username=username,password=password)
        if user :
            login(request,user)
            messages.success(request,"login successfully.")
            return redirect("/")
        else:
            messages.error(request,"Invalid username or password")
 
    return render(request,'login.html')
 
@login_required
def update_profile(request):
    if request.method=="POST":
        data=request.POST
        username=data.get("username")
        first_name=data.get("first_name")
        last_name=data.get("last_name")
        contact_no=data.get("contact_no")
        email=data.get("email")
        profile_pic=request.FILES.get("profile_pic")
        if User.objects.filter(email=email):
            messages.error(request,"User with this email already exits")
        elif User.objects.filter(username=username):
            messages.error(request,"User with this username already exists")
        user=request.user
        user.first_name=first_name
        user.last_name=last_name
        user.username=username
        user.save()
        profile=Profile.objects.filter(user=request.user).first()
        profile.profile_pic=profile_pic
        if contact_no:
            profile.contact_no=contact_no
        profile.save()
        messages.info(request,"User Updated successfully.")
        return redirect("/")
    return render(request,"update.html")
 
@login_required
def forgot_password(request):
    if request.method=="POST":
        user=request.user
        password=request.data.get("password")
        user.set_password(password)
        user.save()
        messages.success("Password changed successfully")
        return redirect("/")
    return render(request, "forgot.html", {})
 
 
@login_required
def user_logout(request):
    logout(request)
    messages.success(request,"Logout succesfully")
    return redirect("login")