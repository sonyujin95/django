from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm  # 로그인 Form : username, password

from .forms import CustomUserCreateForm

# 가입처리 View
# class UserCreateView(CreateView):
#     template_name = 'account/join_form.html'  # GET요청 -> 가입폼 template
#     form_class = CustomUserCreateForm
#     success_url = reverse_lazy('home')  # POST 요청 -> 가입처리 -> 성공후에 redirect 방식으로 이동할 url

# 로그인 처리 View
# class UserLoginView(LoginView):
#     template_name = 'account/login_form.html' 
#     form_class = AuthenticationForm
    # POST : 로그인 처리 - 성공 -> settings.py : LOGIN_REDIRECT_URL에 설정된 url로 이동(redirect)

# 로그아웃 처리 View - LogoutView 사용 => 추가적으로 정의할 것이 없다. ==> urls.py에 직접 등록
# class UserLogoutView(LogoutView):
#     pass
