"""Community URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from com import urls as com_urls
from com import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^com/', include(com_urls)),
    # url(r'login.html/$', views.log_in, name='login'),
    # url(r'register.html/$', views.register, name='register'),
    # url(r'^(?P<question_id>[0-9]+)/question/$', views.answer, name='answer'),
    # url(r'^(?P<question_id>[0-9]+)/keep/$', views.get_keep, name='keep'),
    # url(r'^(?P<question_id>[0-9]+)/poll/$', views.get_poll_question, name='poll'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.question, name='question'),
]
