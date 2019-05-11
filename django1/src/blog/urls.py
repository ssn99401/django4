'''
Created on 2019. 5. 4.

@author: user
'''
from django.urls import path
from blog.views import *

app_name='blog'
#127.0.0.1:8000/blog/
urlpatterns=[
    #뷰 클래스를 url등록시 뷰클래스.as_view()함수로 등록함
        path('', Index.as_view(), name='index'),
        #DetailView를 상속받은 
        path('<int:pk>/', Detail.as_view(), name='detail'),
        path('posting/', Posting.as_view(), name='posting'),
        path('postsearch/', PostSearch.as_view(), name='postsearch')
        
    ]
