from django.urls import path
from . import views

urlpatterns = [
    # exam/hello1 url로 요청이 들어오면 views.hello() 를 호출
    path("hello1", views.hello, name='hello1'),
    path("hello2", views.hello2, name='hello2'),
]