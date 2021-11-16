"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('board/', include('board.urls')),
    path('account/', include('account.urls')),
]
#################################################
# 업로드된 파일을 client가 요청할 수 있도록 처리
#################################################
from django.conf.urls.static import static
from . import settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 어떤 URL로 요청이 들어왔을 때 어떤 경로에 가서 업로드된 파일을 찾을 것인지 등록.