from django.urls import path 
from .views import *
urlpatterns = [
    path('sign-in',signin,name="signin"),
]
