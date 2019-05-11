from django.shortcuts import render
from blog.models import *
'''
클래스 기븐의 뷰를 만들때 , 잘고에서 만든 뷰에 기능을 다루는 클래스를 상속해야함
-> 제네릭뷰 : 장고에서 재공하는 여러가지  상황별 뷰 기능을 구현한 클래스
ex) 모델클래스 객체 목록 기능, 모델클래스의 특정객체 출력기능 , 폼클래스 클래스를 활용하는 기능 
        ,mixing, class based view, overview ...
'''

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from blog.forms import PostingForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse

#글 목록
'''
ListView : 특정 모델클래스의 객체 목록을 다루는 기능이 구현된 뷰
대표적으로 설정할 수 있는 변수
template_name : 사용할 HTML파일 경로
model : 연동할 모델클래스
context_object_name : 객체 리스트 HTML에서 받을 때 사용할 변수 이름
paginate_by : 한페이지에 몇개의 객체를 출력할지 설정하는 변수
'''

class Index(ListView):
    template_name = 'blog/index.html' #render함수의 2번째
    model = Post
    context_object_name = 'objs' #render함수의 3번째의 key값
    paginate_by = 5

#글 상세보기
'''
DetailView : 데이터베이스에 특정 모델클래스에서 한개의 객체를 추출하는 제네릭뷰
단, 해당 뷰클래스를 등록할 때, pk 매개변수에  id값을 넘겨주도록  URL등록을 해야함

template_name, model, context_object_name (공통)
''' 
class Detail(DetailView):
    template_name = 'blog/detail.html' #render함수의 2번째
    model = Post
    context_object_name = 'p'
    
    
#글 쓰기
'''
Formview : 폼클래스를 기반으로 사용자에게 입력공간을 제공 (GET방식)하고, 사용자가 입력한 데이터를 바탕으로 
객체를 생성(POST 방식)을 처리해주는 제네릭뷰  

template_name, context_object_name (공통)
form_class : 연동할 폼클래스를 저장하는 변수

Posting에서는 Post객체 뿐 아니라 사용자가 보낸 파일정보를 바탕으로 PostImage, PostFile 객체로 
생성해야하기 때문에 POST방식 요청에 대한 함수를 오버라이딩해서 기능을 바꿔야함

뷰함수의 데코레이터 기능을 뷰클래스는 XXXMixin 클래스를 상속하는 것으로 대체
데코레이터 하수인 Login_required 대신 LoginRequiredMixin 클래스르 생속하는 것으로 대체
주의할 점! , XXXMixin클래스 상속시, 제네릭뷰보다 먼저 상속해야함
'''
class Posting(LoginRequiredMixin, FormView):
    template_name = 'blog/posting.html'
    context_object_name = 'form'
    form_class = PostingForm
    #POST 방식 요청에 대한 함수를 오버라이딩
    #사용자 입력이 유효한 경우 호출되는 함수 -> form_vaild함수를 오버라이딩    
    #form_valid의 form 매개변수 : 사용자 입력을 기반으로 생성된 form_class 객체
    def form_valid(self, form):
        #form 객체를 기반으로 Post 객체 생성
        p = form.save(commit=False)
        #-> u 변수가 비어있기 때문에 데이터베이스에 저장할 수 없음
        #생성된 Post객체의 빈값 채우기(u 변수)
        #뷰함수에서 클라이언트가 접속한 유저정보 : request.user
        #뷰클래스에서 request변수는 self.request로 꺼낼 수 있음
        #해당 요청을 보낸 클라이언트의 유저정보를 Post 객체의 u변수에 저장
        p.u = self.request.user
        #데이터베이스에 저장
        p.save()
        #사용자가 첨부한 파일/이미지 데이터 마다 PostFile, PostImage 객체를 생성 및 데이터베이스에 저장
        #사용자가 첨부한 파일정보는 request.FILES(사전형) 변수가 저장함
        #FILES에 데이터를 꺼낼때는 <input>태그의 name속성값으로 꺼낼수 있음
        for f in self.request.FILES.getlist('files'):
            pf = PostFile()
            pf.p = p #새로 생성된 Post객채를 대입
            pf.f = f #첨부한 파일데이터를 파일필드에 대입
            pf.save()
        for f in self.request.FILES.getlist('images'):
            pf = PostImage()
            pf.p = p #새로 생성된 Post객채를 대입
            pf.i = f #첨부한 파일데이터를 파일필드에 대입
            pf.save()
        #생성된 글 상세보기하는 URL을 리다이렉트
        return HttpResponseRedirect(reverse('blog:detail', args=(p.id,)))


#검색
#특정조건을 만족하는 Post객체를 리스트로 추출 후 화면에 출력
class PostSearch(ListView):
    template_name = 'blog/postsearch.html'
    model = Post
    context_object_name = 'objs'
    
    #사용자가 입력한 데이터를  포함한 Post객체가 추출되도록 get_queryset함수를 오버라이드
    #get_queryset 함수 : 특정 모델클래스에서 객체를 꺼낼때 어떤 조건으로 꺼내야하는지 설정할수 있는 함수
    #기본값: 모든 객체를 추출하는 모델클래스.objects.all()함수
    def get_queryset(self):
        
        #사옹자가 <form>으로 넘겨준 데이터 중 'search'이름으로 날라온 데이터 추출
        #self.kwargs : GET이나 POST로 넘겨준 <form>태그의 추가 데이터 저장 변수
        print('사용자가 넘겨준 데이터: ',self.request.GET)
        #s = self.kwargs['search']
        s = self.request.GET.get('search', '')
        #추출한 데이터가 빈 문자열인지 확인
        if s:
        #빈문자열이 아닌 경우 Post.objects.filter()함수를 사용해서 검색어 맞는 객체 추출
        #filter(변수__조건 = 값) : 모델클래스 객체들이 특정 변수에 특정조건을 
        #만족하는 확인해  만족하는 객체를 리스트형태로 반환하는  함수
        #조건에 들어가는 명령어는 django라이브러리에서 지정함
        #icontains : 특정변수에 우변에 값이 표함되있으면 객체를 추출하도록 설정하는 조건 i는 대소문자 구분하지않느다는 뜻
        #사용자가 입력한 키워드 (s 변수)를 제목에 포함하느 Post객체를 추출
            objs = Post.objects.filter(title__icontains = s)
        else: #사용자가 키워드를 입력하지 않은 경우의 처리
            objs = Post.objects.all()
    #추출한 데이터를 return으로 반환
        return objs





'''
쿼리셋이란?? 특정 조건을 만족하는 객체를 가져오기 위한 것, sql의 select문에 해당 적절한 퀴리셋으로 얻고자 하는 데이터를 추출해야함
objects.get() 같은 것을 가져올 때 
'''



