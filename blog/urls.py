from django.contrib import admin
from django.urls import path,include
from . import views
 
urlpatterns = [
    path("create_blog",views.create_blog,name="create_blog"),
    path("",views.get_blog,name="home"),
    path("search",views.home_search,name="home_search"),
    path("view_blog/<int:blog_id>/",views.view_blog,name="view_blog"),
    path("update_blog/<int:blog_id>/",views.update_blog,name="update_blog"),
    path("delete_blog/<int:blog_id>/",views.delete_blog,name="delete_blog"),
    path("add_comment/<int:blog_id>/",views.add_comment,name="add_comment"),
    path("update_comment/<int:c_id>/",views.update_comment,name="update_comment"),
    path("delete_comment/<int:c_id>/",views.delete_comment,name="delete_comment")
 
]