# board/forms/py - Board에서 사용할 Form/Model을 구현할 모듈
from django import forms
from .models import Post

# Form field : 사용자로부터 입력받는 부분
#   - label, widget(입력양식), 에러메세지
# class PostForm(forms.Form):
#     title = forms.CharField()  # 텍스트를 입력받는 input (input type='text)
#     content = forms.CharField(widget=forms.PasswordInput)  # textarea



# Form Field들을 Model을 이용해서 구현하는 Form
#   + save() : insert/update
class PostForm(forms.ModelForm):

    class Meta:
        model = Post  # Form 필드를 만들 때 참조/save()시 Model 클래스 지정.
        exclude = ['writer']  # Post의 필드들 중에서 writer를 제외한 나머지를 Form에서 사용.
        # fields = "__all__"
        # fields = ['title', 'content']  # 두개 field만 생성
        # exclude = ['category']  # category 뺀 나머지 Field들 생성
        # fields: 모델의 Field중에서 Form Field로 사용할 Field 목록을 지정
        #   - model의 모든 필드들을 사용할 경우 "__all__"을 지정.
        #   - model의 필드들을 몇몇개만 지정할 경우
        #       - fields=['필드명', ...]
        #       - execlude=['제외할 필드명', ...]