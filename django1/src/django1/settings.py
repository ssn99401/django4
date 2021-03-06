"""
Django settings for django1 project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

from django.urls.base import reverse_lazy


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^7ukjwq%lj^3-m-8ey^m_ei0lhbw7rv46k_12lcem8nei8zw=q'

# SECURITY WARNING: don't run with debug turned on in production!

#서버에러나 page not found 에러등이 안보이도록 개발자 모드설정 변수
#DEBUG = True : 개발자 모드
#DEBUG = False : 배포모드 (에러가 숨겨짐)
DEBUG = True 

#127.0.0.1 대신 사용할 외부 도메인 주소를 저장하는 변수
#ALLOWED_HOSTS = ['.pythonanywhere.com']
'''
reverse와 reverse_lazy 공통점
등록된 URL의 별칭을 바탕으로 URL 문자열을 반환하는 함수
차이점 - URL 문자열을 반환하는 시기 
reverse : 함수 호출이 되자마자 등록된 URL에서 찾음
reverse_lazy : 서버가 정상적으로 실행된 뒤에 URL을 찾음
setting.py는 웹서버 실행에 필요한 변수값을 읽는 단계이므로, reverse_lazy함수를 사용해야함
헷갈린다 -> 무조건 reverse_lazy함수 사용
'''
#LOGIN_URL = reverse_lazy('cl:signin')
#소셜로그인을 마친후 이동할 페이지 주소
#LOGIN_REDIRECT_URL = '/vote/' #reverse_lazy('vote:index')

#social_django 어플리케이션으로  Google-plus 로그인에 사용되는 ID와 보안비밀을 저장하는 변수
#SOCIAL_AUTH_GOOGLE_PLUS_SECRET ='DY8i4WF9zf4TMqns2ilAe8YQ'
#SOCIAL_AUTH_GOOGLE_PLUS_KEY ='713391285577-ind90ksag6pt0m81ndt68db9cg8roai9.apps.googleusercontent.com' 

#로그인처리에 사용되는 클래스를 등록하는 변수
#-> 소셜로그인과 장고의 Auth 어플리케이션의 User 모델클래스를 연동하기 위함
'''AUTHENTICATION_BACKENDS = (
    #구글로그인 사용하기 위한 클래스
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GooglePlusAuth',
    #소셜로그인 정보를 User모델클래스에 저장처리 해주는 클래스
    'django.contrib.auth.backends.ModelBackend',
    
    )
'''
# Application definition
AUTH_USER_MODEL='customlogin.user'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vote',
    'customlogin',
    #social-auth-app-django를 설치했을 때 사용할 수 있는 어플리케이션
    #social_django : 소셜로그인 기능을 다루는 어플리케이션
    #소셜로그인 : 다른 사이트에 회원정보를 우리 웹서버에 가져오는 방식
    #'social_django'
    'blog',
    'cal.apps.CalConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

'''
사용자가 업로드한 미디어파일(이미지 또는 첨부파일)을 다운받을 수 있도록 URL과 웹서버 하드디스크에 경로를 매칭해야함
MEDIA_URL : 클라이어트가 특정 URL주소로 서버에 요청하면 뷰함수 호출이 아닌 파일다운로드 요청을 처리하도록 설정하는 변수
MEDIA_ROOT : 클라이언트가 파일 다운로드 요청을 했을 때, 하드디스크의 어떤 폴더에서 파일을 가져올지 경로를 저장하는 변수

'''
#127.0.0.1:8000/files/로 시작하는 클라이언트의 요청이 파일을 다운받을 수 있도록 설정
MEDIA_URL = '/files/'
#클라이언트가 파일요청시 프로젝트 폴더/files/에서 파일을 꺼내옴
MEDIA_ROOT = os.path.join(BASE_DIR,'files')











