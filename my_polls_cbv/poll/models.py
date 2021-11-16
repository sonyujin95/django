from django.db import models

# Question (질문) 테이블과 연결된 모델 클래스
    # - question_text: 질문내용 - varchar
    # - pub_date: 등록 일시 - datetime
    # - id(PK-자동생성): 1씩 자동증가하는 값


# 모델클래스
    # - models.Model 를 상속
    # - 컬럼 관련 변수들을 class변수로 정의 => Field
    # - class 이름 : 테이블명으로 이름 지정. Pascal 표기법을 사용.
class Question(models.Model):
    # Field 클래스 변수: 변수명-컬럼명, 값-Field객체=>데이터타입, 추가설정
    # Primary Key 컬럼을 생략 -> 자동으로 id라는 이름의 정수형 컬럼이 생성이 된다.
    question_text = models.CharField(max_length=200)  # CharField: 문자열(varchar)
    pub_date = models.DateTimeField(auto_now_add=True)  # DateTimeField: 일시타입(Date) - auto_now_now: insert 될 때의 일시를 자동으로 등록

    def __str__(self):
        return self.question_text

# Choice - 보기
    # - choice_text: 보기 내용 - varchar
    # - vote: 몇번 선택되었는지 - int(number)
    # - question: 어떤 질문에 대한 보기인지. - Question의 Foreign key 컬럼
    # - id (PK - 자동증가)

class Choice(models.Model):
    # Field
    Choice_text = models.CharField(max_length=200)
    vote = models.PositiveIntegerField(default=0)  # PositiveIntegerField: 양수 정수타입. default - 기본값 지정
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    # ForeignKey: ForeignKey 필드선언. to: 부모테이블, on_delete: 참조 데이터 삭제 시 어떻게 할 것인지 지정. CASCADE: 부모테이블 데이터 삭제 시 참조 데이터도 삭제
    def __str__(self):
        return self.Choice_text

# 모델클래스를 작성/변경
# python manage.py makemigrations : DB에 테이블을 어떻게 만들지 정의
# python manage.py migrate : DB에 적용(테이블 생성, 변경)
