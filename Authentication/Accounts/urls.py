from django.urls import path
from . import views

urlpatterns=[
    path("",views.register,name="register"),
    path("login",views.signin,name="signin"),
    path("logout",views.log_out,name="log")
]