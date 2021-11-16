# account/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# 사용자 정의 User Model 정의
#   - AbstractUser 상속해서 구현 : 기존 User Model(username/password) + 추가 Field들 정의
#   - config/settings.py 에 이 클래스를 등록 (AUTH_USER_MODEL 변수에 등록)
#   - admin.py 에 등록 => 관리자 화면 설정
#   - python manage.py makemigrations, migrate

# username, password + name(이름), email(이메일주소), gender(성별)
class CustomUser(AbstractUser):

    # 추가할 Model Field들을 정의
    GENDER_CHOICE = [
        ['M', '남성'],  # <option value='M'>남성</option> [전송할 값, 보여질 값]
        ['F', '여성'],
    ]
    name = models.CharField(max_length=100, verbose_name="이름")
    # EmailField: CharField(varchar) + 이메일형식 검증이 추가. @
    email = models.EmailField(max_length=100, verbose_name='이메일주소')
    gender = models.CharField(max_length=1, verbose_name='성별', choices=GENDER_CHOICE)  # M/F

    def __str__(self):
        return f"{self.pk}. {self.name}"