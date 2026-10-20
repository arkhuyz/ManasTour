from django.urls import path 
from .views import ( login_view, register_view, profile_view, logout_view, ) 
from . import views

app_name = "registration" 

urlpatterns = [ 
      path("login/", login_view, name="login"), 
      path("register/", register_view, name="register"), 
      path("profile/", profile_view, name="profile"),
      path("logout/", logout_view, name="logout"), 
      path("profile/edit/",views.edit_profile_view,name="edit_profile")
      ]