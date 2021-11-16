from django.urls import path
from django.utils.regex_helper import normalize

# View모듈 import
from . import views

# 요청 url - 함수 매핑 => urlpatterns 변수의 리스트에 등록
app_name = 'poll'
urlpatterns = [
    path("list", views.list, name='list'),  # poll/list => views.list함수 호출
    path("vote_form/<int:question_id>", views.vote_form, name = 'vote_form'),  # poll/vote_form => view.vote_form 함수 호출
    path("vote", views.vote, name='vote'),  # poll/vote
    path("vote_result/<int:question_id>", views.vote_result, name='vote_result'),
]

# 사용자 요청 url - http://ip:port/resource_path
# urls.py 에 등록: resource_path
# resource_path: app_root/나머지_path
# config/urls.py : app_root/(poll/) => poll/urls.py 에서 나머지_path를 확인
# polls/urls.py : 나머지_path => view함수를 mapping