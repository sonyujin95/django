from django.shortcuts import render
from django.http import HttpResponse, response
from datetime import datetime

# View 함수
# - View: 사용자 요청을 받아서 처리하는 함수

def hello(request):
    # 사용자 요청을 받아서 "인사말과 현재 날짜와 시간" 을 알려주는 View
    # 현재 날짜/시간 조회
    curr = datetime.now()
    # 응답할 html text를 생성
    txt = """
    <html>
        <body>
            안녕하세요. 반갑습니다.<br>
            현재일시: {}
        </body>
    </html>
    """
    response_txt = txt.format(curr)

    # HttpResponse 생성
    response = HttpResponse(response_txt)
    return response



def hello2(request):
    curr = datetime.now()
    curr_txt = curr.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')

    response = render(request, "exam/greeting.html", {'current':curr_txt})
    return response