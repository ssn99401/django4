'''
Created on 2019. 4. 28.

@author: user
'''
from customlogin.views import *
from django.urls import path
app_name='cl'
#127.0.0.1:8000/login/
urlpatterns=[
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/',signout, name='signout')
    ]