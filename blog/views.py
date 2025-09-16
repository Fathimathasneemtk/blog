from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user.models import Profile
from django.core.paginator import Paginator
 
from blog.forms import *
from blog.models import Blog
 
# Create your views here.
@login_required
def create_blog(request):
    if request.method=="POST":
        form=BlogForms(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            messages.error(request,f"{form.errors}")
 
    return render(request, "create_blog.html", {})
 
 
@login_required
def get_blog(request):
    blogs=[]
    user=request.user
    profile=Profile.objects.filter(user=user).first()
    if profile.type=="admin":
        blogs=Blog.objects.all()
    elif profile.type=="user":
        blogs=Blog.objects.filter(created_by=user.profile)
    paginator=Paginator(blogs,4)
    page_number=request.GET.get("page")
    page=paginator.get_page(page_number)
 
    return render(request,'home.html',{"blogs":blogs,'page':page})
 
@login_required
def home_search(request):
    if request.method=="POST":
        query=request.POST.get("query")
        profile=request.user.profile
        blogs=Blog.objects.filter(title__icontains=query)
        if profile.type=="user":
            blogs=blogs.filter(created_by=profile)
 
        paginator=Paginator(blogs,4)
        page_number=request.GET.get("page")
        page=paginator.get_page(page_number)
 
        return render(request,'home.html',{"blogs":blogs,'page':page})
 
 
 
 
@login_required
def view_blog(request,blog_id):
    blog=Blog.objects.filter(id=blog_id).first()
    user=request.user.profile
    comments=[]
    if user.type=="admin":
        comments=Comment.objects.filter(blog_id=blog_id)
    elif user.type=="user":
        comments=Comment.objects.filter(blog_id=blog_id,user=user)
    return render(request, "view_blog.html", {'blog':blog,'comments':comments})
 
 
@login_required
def update_blog(request,blog_id):
    blog=Blog.objects.filter(id=blog_id).first()
    profile=request.user.profile
    if request.method=="POST":
        if profile.type.lower() in ["admin","user"]:
            form=BlogForms(request.POST,request.FILES,instance=blog)
            if form.is_valid():
                form.save()
                return redirect("view_blog",blog_id=blog.id)
            else:
                messages.error(request,f"{form.errors}")
        else:
            messages.error(request,"You dont have the permission to update")
 
    return render(request, 'update_blog.html',{'blog':blog})
 
 
 
 
@login_required
def delete_blog(request,blog_id):
    profile=request.user.profile
    if profile.type.lower() in ["admin","user"]:
        blog=Blog.objects.filter(id=blog_id).first()
        if blog:
            blog.delete()
            messages.info(request,"blog deleted successfully.")
    else:
        messages.error(request,"You dont have the permission to delete")
    return redirect("/")
 
 
@login_required
def add_comment(request,blog_id):
    profile=request.user.profile
    if request.method=="POST":
        if profile.type.lower() in ["admin","user"]:
            form=CommentForm(request.POST)
            if form.is_valid():
                form.save()
        else:
          messages.error(request,"You dont have the permission to add comment")
    return redirect("view_blog",blog_id=blog_id)
 
 
 
@login_required
def update_comment(request,c_id):
    profile=request.user.profile
    comment=Comment.objects.filter(id=c_id).first()
    if request.method=="POST":
        if profile.type.lower() in ["admin","user"]:
            form=CommentForm(request.POST,instance=comment)
            if form.is_valid():
                form.save()
        else:
            messages.error(request,"You dont have the permission to update comment")
    return redirect("view_blog",blog_id=comment.blog.id)
 
 
@login_required
def delete_comment(request,c_id):
    profile=request.user.profile
    comment=Comment.objects.filter(id=c_id).first()
    if profile.type.lower() in ["admin","user"]:
        if comment:
            blog_id=comment.blog.id
 
            comment.delete()
    else:
         messages.error(request,"You dont have the permission to update comment")
 
    return redirect("view_blog",blog_id=blog_id)
 
 