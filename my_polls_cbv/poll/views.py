from django.shortcuts import redirect, render
from django.urls import reverse  # urls.py에 등록된 path 이름을 이용해 url을 생성하는 함수

from django.views.generic import ListView, View, DetailView
# 모델클래스들 import
from .models import Question, Choice


# 설문 목록(List) 보기 처리 View Class
# 목록(List)관련된 View는 ListView를 상속받아서 구현
class QuestionListView(ListView):
    model = Question  # 전체 데이터를 조회할 모델클래스를 설정
    template_name = 'poll/list.html'  # 응답할 template 파일 경로를 지정.
    # 조회결과를 template에게 전달(context_data, context_object)
    # name: object_list, 모델클래스이름_list (클래스이름을 소문자로 변경)
    # 원하는 이름을 지정: context_object_name = '원하는name'

# 투표작업 처리하는 View
# 동일한 URL 요청
# - GET 요청: 폼을 전달
# - POST 요청: 투표 처리

class VoteView(View):
    # GET 요청 처리
    def get(self, request, *args, **kwargs):
        # **kwargs: path parameter을 조회.
        question_id = kwargs['question_id']
        try:
            question = Question.objects.get(pk=question_id)  # get(): 1개조회. 조회결과가 없거나(0) 2개이상인경우 Exception 발생.
            return render(request, 'poll/vote_form.html', {"question":question})
        except:
            # 없는 question_id로 조회한 경우 => 사용자가 없는 id의 설문을 요청
            return render(request, 'poll/error_page.html', {"error_message":"없는 설문번호를 요청했습니다."})


    # POST 요청 처리
    def post(self, request, *args, **kwargs):
        # 요청파라미터 조회: choice=id, question_id=id
        # choice_id = request.POST['choice']
        choice_id = request.POST.get('choice')
        question_id = request.POST['question_id']  # kwargs['question_id']

        if choice_id == None:  # 보기를 선택하지 않고 조회한 경우. => vote_form.html을 호출
            question = Question.objects.get(pk=question_id)
            return render(request, "poll/vote_form.html", {'question':question, "error_message":"보기를 선택하세요"})

        # 요청파라미터 검증(validation) - 필수 요청파라미터가 잘 전송되었는지 체크


        print("vote(): ", choice_id, question_id)
        # Choice를 update   update choice set vote = vote + 1 where id = 선택된 id
        # 1. Choice 조회. 2. vote 변경, 3. save()
        choice = Choice.objects.get(pk=choice_id)
        choice.vote = choice.vote + 1
        choice.save()

        # url = f"/poll/vote_result/{question_id}"
        url = reverse("poll:vote_result", args=[question_id])  # ("path name", args=[path 파라미터에 전달할 값, ...])
        print('------------------redirect url: ', url)
        return redirect(to=url)


# DetailView: 특정 모델의 primary key 값을 path parameter로 받아서 조회한 결과를 template에 전달하면서 호출.
# pk를 받는 path parameter: urls.py url경로/<타입:pk>
# context_data의 name: 'object', '모델클래스이름'-소문자. context_object_name:원하는이름
class QuestionDetailView(DetailView):
    model = Question
    template_name = 'poll/vote_result.html'
    # context_object_name="q"






