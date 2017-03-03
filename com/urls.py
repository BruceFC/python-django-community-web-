from django.conf.urls import url
from com import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login.html/', views.log_in, name='login'),
    url(r'register.html/$', views.register, name='register'),
    url(r'logout/$', views.log_out, name='logout'),
    url(r'^(?P<question_id>[0-9]+)/$', views.question, name='question'),
    url(r'quiz/', views.quiz, name='quiz'),
    url(r'user/$', views.user, name='user'),
    url(r'search/$', views.search, name='search'),  # 搜索
    url(r'(?P<question_id>[0-9]+)/q_keep/$', views.q_keep, name='q_keep'),  # question 收藏  动作
    url(r'(?P<question_id>[0-9]+)/keep/$', views.keep, name='keep'),  # index 收藏  动作
    url(r'keep_page/$', views.keep_page, name='keep_page'),  # 进入收藏列表页
    url(r'answered_page/$', views.answered_page, name='answered_page'),  # 进入回答记录页
    url(r'my_quized/$', views.my_quiz, name='my_quiz'),  # 进入我的提问记录页
    url(r'(?P<question_id>[0-9]+)/keep_del/$', views.keep_del, name='keep_del'),
    url(r'(?P<answer_id>[0-9]+)/answer_del/$', views.answer_del, name='answer_del'),
    url(r'(?P<question_id>[0-9]+)/quiz_del/$', views.quiz_del, name='quiz_del'),
    url(r'setting/$', views.setting, name='setting'),
    url(r'set_pd/$', views.set_password, name='set_password'),
    url(r'upload/$', views.head_img, name='head_img'),  # 上传头像
    # url(r'^(?P<question_id>[0-9]+)/answer/$', views.answer, name='answer'),
    # url(r'^(?P<question_id>[0-9]+)/keep/$', views.get_keep, name='keep'),
    # url(r'^(?P<question_id>[0-9]+)/poll/$', views.get_poll_question, name='poll'),
]
