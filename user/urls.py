from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.user_register,name="user_register"),
    path('login/',views.user_login,name="login"),
    path("update_profile/",views.update_profile,name="update_profile"),
    path("forgot_password/",views.forgot_password,name="forgot_password"),
    path("logout/",views.user_logout,name="logout")

]
