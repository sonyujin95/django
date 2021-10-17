from django.urls import path
from django.utils.regex_helper import normalize

# View모듈 import
from . import views

# 요청 url - 함수 매핑 => urlpatterns 변수의 리스트에 등록
app_name = 'poll'
urlpatterns = [
    path("list", views.QuestionListView.as_view(), name='list'),  # poll/list => views.list함수 호출
    path("vote/<int:question_id>", views.VoteView.as_view(), name = 'vote'),  # poll/vote_form => view.vote_form 함수 호출
    path("vote_result/<int:pk>", views.QuestionDetailView.as_view(), name='vote_result'),
]

# View 클래스.as_view() :
#   1. View 클래스의 객체를 생성해서 등록(장고 실행환경)
#       - class 변수를 이용해 설정들만 할 경우에 그 설정을 as_view() 메소드에 지정할 수 있다.
#   2. list url 요청들어오면 1에서 생성된 객체의 dispatch() 메소드를 호출
#       - dispatch() - GET 요청일 경우에 get() 메소드를 POST 요청일 경우에 post() 메소드를 호출

# from models import Question
# from django.views.generic import ListView, DetailView
# urlpatterns = [
#     path("list", ListView.as_view(model=Question, template_name='poll/list.html'), name='list'),  # poll/list => views.list함수 호출
#     path("vote/<int:question_id>", views.VoteView.as_view(), name = 'vote'),  # poll/vote_form => view.vote_form 함수 호출
#     path("vote_result/<int:pk>", DetailView.as_view(model=Question, template_name='poll/vote_result.html'), name='vote_result'),
# ]




# 사용자 요청 url - http://ip:port/resource_path
# urls.py 에 등록: resource_path
# resource_path: app_root/나머지_path
# config/urls.py : app_root/(poll/) => poll/urls.py 에서 나머지_path를 확인
# polls/urls.py : 나머지_path => view함수를 mapping