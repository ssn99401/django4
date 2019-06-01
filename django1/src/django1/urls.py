"""django1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include ###include중요
from vote.views import main
#기본 도메인이 웹서버가 실행되는 환경에 맞춰짐
#개발 과정에서의 기본 도메인 주소 : 127.0.0.1:8000/
'''
urls.py : 만들어진 뷰 함수/클래스를  URL에 등록하는 공간
path(요청할 URL주소, 호출된 함수/클래스)
urlpatterns : 처리할 수 있는 URL-뷰를 저장하는 변수

'''
urlpatterns = [
    path('admin/', admin.site.urls),
    #http://127.0.0.1:8000/ 입력 시, main 뷰 함수가 호출됨
    path('', main),
    #127.0.0.1:8000/vote/로 시작하는 모든 요청들을, vote폴더의 urls.py에서 관리하도록 등록하는 과정
    path('vote/', include('vote.urls')),
    path('login/', include('customlogin.urls')),
    #social_django 폴더의 urls.py를 등록
    #다른 개발자가 만든 어플리케이션의 urls.py를 등록하고 사용할 때,
    #app_name 설명이 있었는데 모르겠다...
    #-> include함수의 namespace 매개변수에 원하는 그룸명 지정
    #path('social/', include('social_django.urls',namespace='social')),
    path('blog/', include('blog.urls')),
    path('', include('cal.urls')),
]
#사용자가 이미지, 첨부파일 요청 URL을 사용하면, 서버의 하드디스크에 파일을 HTTP로 넘겨줄수 있도록 등록하는 작업
from django.conf import settings
from django.conf.urls.static import static

#path 함수대신, static함수를 사용
#127.0.0.1:8000/files/ 로 시작하는 요청은 프로젝트 폴더/files/에서 파일을 꺼내도록 URL등록
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)






