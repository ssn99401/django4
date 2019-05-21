from django.shortcuts import render, get_object_or_404
from vote.models import Question, Choice
from django.contrib.auth.decorators import login_required
'''decorator : 뷰함수가 실행되기 전에 먼저 실행되는 함수
login_required : 뷰함수가 실행되기전 웹클라이언트의 로그인 여부를 파악하고 
비로그인상테인 웹클라이언트에게 로그인 페이지를 리다이렉스 해주는 데코레이터

데코레이터를 뷰함수에 적용하는 방법
#@적용할 데코레이터
def 뷰함수()
'''

def main(request):
    return render(request,'main.html',{})
#설문조사 리스트가 뜨는 메인페이지
def index(request):
    #데이터베이스에 저장된 Question 객체 리스트로 추출
    a = Question.objects.all()
    #날씨정보 전달
    api_date, api_time = get_api_date()
    url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?"
    key = "serviceKey=" + "DQdkxZWqaYrA0zeZ0s3qc93jqj3ubKvUE3Q7hrBQVa8mhXiTgknQTNW%2FPZ2IZxvUuDZy%2FdVeNvIRgkIz%2FgEjiA%3D%3D"
    date = "&base_date=" + api_date
    time = "&base_time=" + api_time
    nx = "&nx=97"
    ny = "&ny=76"
    numOfRows = "&numOfRows=100"
    type = "&_type=json"
    api_url = url + key + date + time + nx + ny + numOfRows + type

    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_json = json.loads(data,encoding='utf8')

    parsed_json = data_json['response']['body']['items']['item']

    target_date = parsed_json[0]['fcstDate']  # get date and time
    target_time = parsed_json[0]['fcstTime']

    date_calibrate = target_date  # date of TMX, TMN
    if target_time > 1300:
        date_calibrate = str(int(target_date) + 1)

    passing_data = {}
    for one_parsed in parsed_json:
        if one_parsed['fcstDate'] == target_date and one_parsed['fcstTime'] == target_time:  # get today's data
            passing_data[one_parsed['category']] = one_parsed['fcstValue']

        if one_parsed['fcstDate'] == date_calibrate and (
                one_parsed['category'] == 'TMX' or one_parsed['category'] == 'TMN'):  # TMX, TMN at calibrated day
            passing_data[one_parsed['category']] = one_parsed['fcstValue']
    rain = passing_data['PTY']

    #index.html 전달
    return render(request, 'vote/index.html',{'rain':rain,'a':a})
#설문조사 페이지
def detail(request,q_id):
    #Question객체들 중 q_id와 동일한 값을 id변수에 가진 객체 추출
    #또는 조건에 맞는 객체가 없으면 404번에러를 클라이언트에게 전달
    q = get_object_or_404(Question, id=q_id)
    '''
    get_object_or_404(모델클래스, 조건) : 모델클래스에 조건을 검색해 1개의 객체 추출
    만약 객체가 없는경우, 클라이언트의 잘못된 접근으로 판단해 뷰함수를 종료하고 404번에러를 전달
    
    현재 Question 모델클래스는 Choice 모델클래스가 외래키로 연결한 상태이므로, 
    Question 객체들은 자신과 연결된 Choice 객체들을 추출할 수 있음.
    Question객체.choice_set.all(또는 get,filter,exclude)로 데이터베이스에 저장된
    Choice 객체 추출 가능. 모델클래스 이름을 소문자로 작성해야함
    '''
    #Question 객체로 연결된 Choice 객체들을 모두 추출
    c_list = q.choice_set.all()
    #HTML 파일 전달 
    return render(request,'vote/detail.html',{'q':q, 'c_list':c_list})

from django.http.response import HttpResponseRedirect
'''
HttpResponseRedirect(URL 주소)
: 웹클라이언트가 HTML파일을 받는것이 아닌, 새로운 URL주소를 받아 재요청을
할 수 있도록 처리할 수 있는 클래스.

Redirect : 웹서버가 300번대 코드를 전달하면서 더 처리해야할 요청을
웹 클라이언트에게 전달하는 응답

사용방법
return HttpResponseRedirect(이동할 URL 주소)
'''


#투표 반영
def vote(request):
    #사용자의 요청이 POST방식인지 확인
    #request.method : 웹클라이언트의 요청방식을 저장한 변수
    #"GET", "POST" 문자열을 저장하고 있음
    if request.method == "POST":
        '''
        request.POST 또는 request.GET : 웹클라이언트의 요청과 함께 날라온 데이터를
        저장하는 변수
        값을 꺼낼때, HTML 코드에 name 속성 이름으로 값을 추출할 수 있음
        '''
        print(request.POST)
        #사용자가 투표한 Choice객체의 id값을 추출
        c_id = request.POST.get('vote')
        #id값을 바탕으로 데이터베이스에 Choice 객체 추출
        c = get_object_or_404(Choice, id=c_id)
        #votes 변수에 투표 반영
        c.votes = c.votes + 1
        #데이터베이스에 변경사항 저장
        c.save()
        #다른 뷰함수의 URL을 웹클라이언트에게 전달
        #c.q : Choice객체가 연결한 Question객체 변수
        #c.q.id : 연결한 Question객체의 id변수값
        url = '/vote/result/%s/' % c.q.id
        return HttpResponseRedirect( url )
#결과 페이지
def result(request, q_id):
    #Question객체를 q_id값으로 한개 추출
    q = get_object_or_404(Question, id=q_id)
    #HTML 전달
    return render(request, 'vote/result.html',{'q': q })
#모델 폼 클래스 임포트
from vote.forms import QuestionForm, ChoiceForm
from datetime import datetime
#Question 객체 추가
@login_required
def qregiste(request):
    #웹클라이언트의 요청방식 구분 -> 하나의 뷰에 두가지 기능을 구현하고자 함
    if request.method == "GET":
        #폼클래스 객체 생성시, 매개변수를 입력하지 않으면 <input>태그에 아무런 값도 채워지지 않는 상태로 생성됨
        #GET방식 요청
            #폼클래스 객체를 생성하고 HTML파일 전달
        obj = QuestionForm()
        '''
        form 객체를 기반으로 HTML 코드에 들어갈 <input> 태그를 생성할 때, as_p(), as_table(), as_ul()함수를 사용 가능
        as_p : 설명과 입력공간이 <p>태그로 묶여있는  HTML코드로 변환
        as_table : 설명과 입력공간이 한 행<tr>에 묶여있는 HTML코드로 변환
        as_ul : 설명과 입력공간이 리스트아이템<li>에 묶여있는 HTML코드로 변환
        '''
        print('as_table() 결과 : ',obj.as_table())
        return render(request,'vote/qregiste.html',{'form':obj.as_table()})
    
    elif request.method == "POST":
        #POST 방식 요청
            #사용자 입력 기반으로 폼클래스 객체 생성
            
        #request.POST : POST요쳥 시 동봉된 사용자의 입력데이터
        obj = QuestionForm(request.POST)
        #폼클래스 객체를 연동된 모델클래스 객체로 변환
            
        #q : 사용자 입력으로 name변수에 값이 채워져 있는 Question객체
        #폼객체.save() : 데이터베이스에 사용자 입력 기반의 새로운 객체가 저장되면서 새로운 객체를 반환하는 함수
        #사용자는 pub_date변수에 기반을 입력할 수 없기에, 폼객체를 바로 데이터베이스에 저장할 수 없음(pub_date변수의 값이 없는 상태)
        #따라서 Question객체로 변환한 뒤, 비어있는 변수를 채워줘야함 -> 폼객체.save(commit=False)
        q = obj.save(commit=False) #모델객체를 만들어주면서 비어있는 칸을 채우기 위해 데이터베이스의 저장안한다는 의미
        #데이터베이스에 저장되지 않은 변수의 id값은 None이 뜬다
        print('저장 전 : ', q.id) 
        #값이 채워져 있지 않은 변수에 값을 채움
        q.pub_date = datetime.now() #컴퓨터의 현재시간/날짜 대입
        #데이터배이스에 새로만든 모델객체 저장
        #모델객체.save() : 새로운 객체를 저장하거나 기존객체의 변수값변경을 데이터베이스에 저장할 수 있음
        q.save()
        print('저장 후: ', q.id)
        #다른 URL로 이동
        return HttpResponseRedirect('/vote/%s/' % q.id)
         
#Question 객체 수정
@login_required
def qupdate(request, q_id):
    #수정할 대상의 객체 추출
    q = get_object_or_404(Question, id = q_id)
    #GET 방식 요청
    if request.method == 'GET':
        #수정할 객체를 기반으로 QuestionForm 객체 생성
        obj = QuestionForm(instance = q)
        #HTML 파일전달
        return render(request,'vote/qupdate.html',{'form':obj.as_p()})
    #POST 방식 요청
    if request.method == 'POST':
        #사용자 입력+수정할 객체를 기반으로 QuestionForm 객체를 생성
        obj = QuestionForm(request.POST, instance=q)
        #수정을 하는 객체를 바탕으로 QuestionForm 객체가 생성됬기 때문에 pub_date변수는 이미 값이 채워져있음
        #->바로 데이터베이스에 저장
        w = obj.save()
        print('수정할 객체 q의 id값 : ',q.id)
        print('폼객체가 준 객체의 id값 : ',w.id)
        #다른 URL에 전달
        return HttpResponseRedirect('/vote/%s/' % w.id)
        
#Question 객체 삭제
@login_required
def qdelete(request, q_id):
    q = get_object_or_404(Question, id=q_id)
    print('삭제전 id : ',q.id)
    q.delete() #데이터베이스에서 삭제됨
    print('삭제후 id : ',q.id)
    return render(request,'vote/delete_com.html',{'title':q.name,'type': 1})

#Choice 객체 추가
@login_required
def cregiste(request):
    #GET 요청
        #ChoiceForm 객체 생성 및 HTML 전달
    if request.method == "GET":
        obj = ChoiceForm()
        return render(request, 'vote/cregieste.html',{'form':obj.as_table()})
    #POST 요청
    elif request.method == "POST":
        #사용자 입력기반으로 ChoiceForm 객체 생성
        obj = ChoiceForm(request.POST)
        #ChoiceForm객체를 기반으로 Choice객체 생성 및 데이터 베이스 저장
        #-> 값이 비어있는 변수가 없기 때문에(votes는 기본값 설정이 되어있음)
        c = obj.save()
        #다른 패이지로 이동(index나 detail로 이동)
        return HttpResponseRedirect('/vote/%s/' %c.q.id)
#Choice 객체 수정
@login_required
def cupdate(request, c_id):
    c = get_object_or_404(Choice, id=c_id)
    if request.method == "GET":
        obj = ChoiceForm(instance=c)
        return render(request,'vote/cupdate.html',{'obj':obj})
    elif request.method == "POST":
        obj = ChoiceForm(request.POST, instance=c)
        obj.save()
        return HttpResponseRedirect('/vote/%s/' % c.q.id)
#Choice 객체 삭제
@login_required
def cdelete(request, c_id):
    #Choice객체 찾기
    c = get_object_or_404(Choice, id=c_id)
    #데이터베이스에서 삭제
    print(c.id)
    c.delete()
    print(c.id)
    #HTML 파일 or URL 주소 전달
    return render(request,'vote/delete_com.html',{'title': c.name,'type': 2})
    
import datetime
import pytz
import urllib.request
import json

def get_api_date():
    standard_time = [2, 5, 8, 11, 14, 17, 20, 23]
    time_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%H')
    check_time = int(time_now) - 1
    day_calibrate = 0
    while not check_time in standard_time:
        check_time -= 1
        if check_time < 2:
            day_calibrate = 1
            check_time = 23

    date_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d')
    check_date = int(date_now) - day_calibrate
    if (check_time < 10):
        return (str(check_date), ('0' + str(check_time) + '00'))
    else:
        return (str(check_date), (str(check_time) + '00'))


def get_weather_data():
    api_date, api_time = get_api_date()
    url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?"
    key = "serviceKey=" + "DQdkxZWqaYrA0zeZ0s3qc93jqj3ubKvUE3Q7hrBQVa8mhXiTgknQTNW%2FPZ2IZxvUuDZy%2FdVeNvIRgkIz%2FgEjiA%3D%3D"
    date = "&base_date=" + api_date
    time = "&base_time=" + api_time
    nx = "&nx=97"
    ny = "&ny=76"
    numOfRows = "&numOfRows=100"
    type = "&_type=json"
    api_url = url + key + date + time + nx + ny + numOfRows + type

    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_json = json.loads(data)

    parsed_json = data_json['response']['body']['items']['item']

    target_date = parsed_json[0]['fcstDate']  # get date and time
    target_time = parsed_json[0]['fcstTime']

    date_calibrate = target_date  # date of TMX, TMN
    if target_time > 1300:
        date_calibrate = str(int(target_date) + 1)

    passing_data = {}
    for one_parsed in parsed_json:
        if one_parsed['fcstDate'] == target_date and one_parsed['fcstTime'] == target_time:  # get today's data
            passing_data[one_parsed['category']] = one_parsed['fcstValue']

        if one_parsed['fcstDate'] == date_calibrate and (
                one_parsed['category'] == 'TMX' or one_parsed['category'] == 'TMN'):  # TMX, TMN at calibrated day
            passing_data[one_parsed['category']] = one_parsed['fcstValue']

    #render(request,'vote/index.html',passing_data)
    






