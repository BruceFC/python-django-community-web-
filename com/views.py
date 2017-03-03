from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Question, Answer, Poll, NewUser, UserProfile, Questioner, Keep, Quiz
from .forms import AnswerForm, LoginForm, RegisterForm, SetInfoForm, SearchForm, QuizForm, PassForm, HeadImgForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt   #
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from PIL import ImageFile  # 上传图片用
import markdown2
from urllib.parse import urlparse


def index(request):
    user = request.user
    allQuestion = Question.objects.all()
    if user is authenticate():
        questions = user.keep.question
        keeplist = []
        for x in allQuestion:
            if x in questions:
                keeplist.append(x)
            # else:
            #     y = 0
        latest_question_list = Question.objects.query_by_time()
        lf = LoginForm()
        context = {'latest_question_list': latest_question_list, 'lf': lf, 'questions': questions, 'keeplist': keeplist}
        return render(request, 'index.html', context)
    else:
        latest_question_list = Question.objects.query_by_time()
        lf = LoginForm()
        context = {'latest_question_list': latest_question_list, 'lf': lf}
        return render(request, 'index.html', context)


@csrf_exempt  # -------------------搜索页--------------------
def search(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        allQuestion = Question.objects.all()
        SearchResult = []
        for x in allQuestion:
            if keyword in x.title:
                SearchResult.append(x)
            elif keyword in x.content:
                SearchResult.append(x)
        SearchStatus = "Error" if len(SearchResult) == 0 else "Success"
        alltext = {"keyword": keyword, "SearchResult": SearchResult, "SearchStatus": SearchStatus}
        return render(request, 'search.html', alltext)
    else:
        print("出错")  # 测试
        return render(request, 'search.html')


def log_in(request):  # -------------------登陆页--------------------
    if request.method == 'GET':
        lf = LoginForm()
        return render(request, 'login.html', {'form': lf})
    if request.method == 'POST':
        lf = LoginForm(request.POST)
        if lf.is_valid():
            username = lf.cleaned_data['username']
            password = lf.cleaned_data['password']  # 获取数据
            # username = request.POST.get('username', '')
            # password = request.POST.get('password', '')  # ---未经验证表单信息获取输入信息---
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                url = request.POST.get('', '/com/')
                return redirect(url)
            else:
                return render(request, 'login.html', {'form': lf, 'error': "账号密码不匹配！"})
        else:
            return render(request, 'login.html', {'form': lf, 'error': "输入不合法！"})


@login_required
def log_out(request):
    url = request.POST.get('', '/com/')
    logout(request)
    return redirect(url)


def register(request):
    if request.method == 'GET':
        rf = RegisterForm()
        return render(request, 'register.html', {'form': rf})
    if request.method == 'POST':
        rf = RegisterForm(request.POST)
        if request.POST.get('raw_username', '') != '':  # 不懂
            try:
                user = NewUser.objects.get(username=request.POST.get('raw_username', ''))
            except ObjectDoesNotExist:
                return render(request, 'register.html', {'form': rf, 'msg': "该用户名可用！"})
            else:
                return render(request, 'register.html', {'form': rf, 'msg': "该用户名已存在！"})

        else:
            if rf.is_valid():
                username = rf.cleaned_data['username']
                filter_result = NewUser.objects.filter(username=username)
                if len(filter_result) > 0:              # 用户名重名
                    return render(request, 'register.html', {'form': rf, 'msg': "该用户名已存在！"})
                else:
                    username = rf.cleaned_data['username']
                # email = rf.cleaned_data['email']
                    password1 = rf.cleaned_data['password1']
                    password2 = rf.cleaned_data['password2']
                if password1 != password2:
                    return render(request, 'register.html', {'form': rf, 'msg': "输入密码不一致！"})
                else:
                    user = NewUser(username=username, password=password1)
                    user.set_password(password1)  # 重要重要重要！！！设置密码加密，不然是明文，admin里密码显示也是明文，登录不了
                    user.save()
                    u = UserProfile.objects.create(user=user, username=username,  # 注册成功则创建对应user profile
                                                   password=password1)
                    u.save()
                    return redirect('/com/templates/login.html', {'form': rf, 's': "注册成功！请登录！"})
            else:
                return render(request, 'register.html', {'form': rf, 'msg': "输入不合法！"})


@login_required
def question(request, question_id):
    """
    try: # since visitor input a url with invalid id
        article = Article.objects.get(pk=article_id)  # pk???
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    """  # shortcut:
    if request.method == 'POST':   # ------------question页面发回答------------
        answerform = AnswerForm(request.POST)
        # url = urlparse('/com/', question_id)
        if answerform.is_valid():
            user = request.user
            User = UserProfile.objects.get(user=user)
            q = Question.objects.get(id=question_id)
            new_answer = answerform.cleaned_data['answer_content']
            a = Answer(content=new_answer, question=q, user=user)  # 创建回答
            a.save()
            q.answer_num += 1
            q.save()
            User.answered_num += 1
            User.save()

            question = get_object_or_404(Question, id=question_id)
            content = markdown2.markdown(question.content, extras=["code-friendly",
                                                                   "fenced-code-blocks",
                                                                   "header-ids",
                                                                   "toc",
                                                                   "metadata"])
            answerform = AnswerForm()
            answers = question.answer_set.all

            return render(request, 'question.html', {
                'question': question,
                'answerform': answerform,
                'content': content,
                'answers': answers,
            })
            # return render(request, 'question.html')
        else:
            p = answerform.errors  # 测试用
            return render(request, 'question.html', {'form': answerform, 'msg': p})

    else:  # --------------------进question页面--method=get---------------
        question = get_object_or_404(Question, id=question_id)
        content = markdown2.markdown(question.content, extras=["code-friendly",
                                                               "fenced-code-blocks",
                                                               "header-ids",
                                                               "toc",
                                                               "metadata"])
        anwserform = AnswerForm()
        answers = question.answer_set.all

        user = request.user
        questions = user.keep_set.all()
        filter_result = questions.filter(question_id=question_id)
        k = len(filter_result)

        return render(request, 'question.html', {
            'question': question,
            'answerform': anwserform,
            'content': content,
            'answers': answers,
            'k': k,
            })


@login_required  # -------------提问页-----------------
def quiz(request):
    if request.method == 'POST':
        qf = QuizForm(request.POST)
        if qf.is_valid():
            a = Questioner.objects.create(name=request.user, password=request.user.password)  # 创建外键
            title = qf.cleaned_data['title']
            content = qf.cleaned_data['content']
            # questioner = request.user  # 错误  questioner是外键 不能用user
            q = Question(title=title, content=content, questioner=a)  # 创建问题
            q.save()
            user = request.user
            User = UserProfile.objects.get(user=user)
            User.quized_num += 1  # 用户创建问题数+1
            User.save()
            z = Quiz.objects.create(user=user, question=q)  # 创建quiz记录
            z.save()
            latest_question_list = Question.objects.query_by_time()
            lf = LoginForm()
            context = {'latest_question_list': latest_question_list, 'lf': lf, 'qf': qf}
            return render(request, 'index.html', context)
        else:
            # p = qf.errors   # 测试、表单验证不通过时返回错误信息
            p = '标题和内容都不能为空！'
            return render(request, 'quiz.html', {'form': qf, 'msg': p})
    else:  # -------------进入提问页-----------------
        return render(request, 'quiz.html')


# @login_required
# def answer(request, question_id):
#     answerform = AnswerForm(request.POST)
#     if request.method == 'POST':
#         answerform = AnswerForm(request.POST)
#         # url = urlparse('/com/', question_id)
#         if answerform.is_valid():
#             user = request.user
#             q = Question.objects.get(id=question_id)
#             new_answer = answerform.cleaned_data['answer_content']
#             a = Answer(content=new_answer, question=q, user=user)  # have tested by shell
#             a.save()
#             q.answer_num += 1
#             return redirect(request, 'question.html', {'form': answerform})
#         else:
#             p = answerform.errors              # 测试用
#             return render(request, 'question.html', {'form': answerform, 'msg': p})


@login_required  # ------------------index.html收藏问题动作-----------------
@csrf_exempt
def keep(request, question_id):
    if request.method == 'POST':
        user = request.user
        User = UserProfile.objects.get(user=user)
        # question = Question.objects.get(id=question_id)
        question = get_object_or_404(Question, id=question_id)
        questions = user.keep_set.all()
        filter_result = questions.filter(question_id=question_id)
        if len(filter_result) > 0:  # 已收藏
            k = Keep.objects.get(user=user, question=question)
            k.delete()
            question.keep_num -= 1
            question.save()
            User.keep_num -= 1
            User.save()
            flag = len(filter_result)
            # return redirect('/com/')  #  重载页面
            # print("it's a test")  # 测试
            # return HttpResponse(question.keep_num)
            result = [question.keep_num, flag]
            return HttpResponse(result)
        else:  # 未收藏
            # if question not in questions:  # ---------------无效---------------
            k = Keep.objects.create(user=user, question=question)
            question.user.add(user)
            k.save()
            question.keep_num += 1
            question.save()
            User.keep_num += 1
            User.save()
            flag = len(filter_result)
            # return redirect('/com/')  #  重载页面
            # print("it's a test")  # 用于测试
            # return HttpResponse(question.keep_num)
            result = [question.keep_num, flag]
            return HttpResponse(result)


@csrf_exempt
@login_required  # ------------------question.html 收藏问题动作-----------------
def q_keep(request, question_id):
    if request.method == 'POST':
        user = request.user
        User = UserProfile.objects.get(user=user)
        # question = Question.objects.get(id=question_id)
        question = get_object_or_404(Question, id=question_id)
        questions = user.keep_set.all()
        filter_result = questions.filter(question_id=question_id)
        if len(filter_result) > 0:  # -----收藏了-----
            k = Keep.objects.get(user=user, question=question)
            k.delete()
            question.keep_num -= 1
            question.save()
            User.keep_num -= 1
            User.save()
            result = len(filter_result)
            return HttpResponse(result)
        else:                       # -----未收藏-----
            k = Keep.objects.create(user=user, question=question)
            question.user.add(user)
            k.save()
            question.keep_num += 1
            question.save()
            User.keep_num += 1
            User.save()
            result = len(filter_result)
            return HttpResponse(result)


@login_required  # -------------待实现-------给回答点赞----------
def get_poll_answer(request, answer_id):
    logged_user = request.user
    answer = Answer.objects.get(id=answer_id)
    polls = logged_user.poll_set.all()
    answers = []
    for poll in polls:
        answers.append(poll.answer)
    if answer in answers:
        url = urlparse('/com/', answer_id)
        return redirect(url)
    else:
        answer.poll_num += 1
        answer.save()
        poll = Poll(user=logged_user, answer=answer)
        poll.save()
        data = {}
        return redirect('/com/')


@login_required  # -------------进入用户个人信息页user.html-----------------
def user(request):
    # if request.method == 'GET':  # 进user页面查看个人信息
        # keep = Keep.objects.get(user=user)
        # person_keep_list = keep.query_by_keeper()
        # return render(request, 'user.html', {'person_keep_list': person_keep_list})
        return render(request, 'user.html')
    # else:


@login_required  # -------------进入用户个人收藏页collection.html-----------------
def keep_page(request):
    # user_id = request.user.id
    # user = NewUser.objects.get(id=user_id) 真蠢
    user = request.user
    person_keep_list = user.keep_set.all()
    return render(request, 'collection.html', {'person_keep_list': person_keep_list})


@login_required # -------------删除个人收藏-----------------
def keep_del(request, question_id):
    user = request.user
    question = get_object_or_404(Question, id=question_id)
    k = Keep.objects.get(user=user, question=question)
    k.delete()
    User = UserProfile.objects.get(user=user)
    User.keep_num -= 1
    User.save()
    question.keep_num -= 1
    question.save()
    person_keep_list = user.keep_set.all()
    return render(request, 'collection.html', {'person_keep_list': person_keep_list})


@login_required  # -------------进入用户个人回答记录页answered.html-----------------
def answered_page(request):
    user = request.user
    person_answered_list = user.answer_set.all()
    return render(request, 'answered.html', {'person_answered_list': person_answered_list})


@login_required  # -------------删除个人回答-----------------
def answer_del(request, answer_id):
    user = request.user
    a = Answer.objects.get(id=answer_id)
    question = a.question
    a.delete()
    User = UserProfile.objects.get(user=user)
    User.answered_num -= 1
    User.save()
    question.answer_num -= 1
    question.save()
    person_answered_list = user.answer_set.all()
    return render(request, 'answered.html', {'person_answered_list': person_answered_list})


@login_required  # -------------进入用户个人提问记录页my_quiz.html-----------------
def my_quiz(request):
    user = request.user
    person_quized_list = user.quiz_set.all()
    return render(request, 'my_quiz.html', {'person_quized_list': person_quized_list})


@login_required  # -------------删除我提出的问题-----------------
def quiz_del(request, question_id):
    user = request.user
    User = UserProfile.objects.get(user=user)
    question = get_object_or_404(Question, id=question_id)
    quiz = get_object_or_404(Quiz, question=question)
    quiz.delete()
    question.delete()
    User.quized_num -= 1
    User.save()
    person_quized_list = user.quiz_set.all()
    return render(request, 'my_quiz.html', {'person_quized_list': person_quized_list})


@login_required  # ----------------修改个人信息-------------------
def setting(request):
    if request.method == 'GET':  # ----------进入setting页面--------------
        return render(request, 'setting.html')
    if request.method == 'POST':
        sf = SetInfoForm(request.POST)  # 括号内容要加 原理？？？
        # pf = PassForm
        if sf.is_valid():
            new_username = sf.cleaned_data['username']
            address = sf.cleaned_data['address']
            job = sf.cleaned_data['job']
            em = sf.cleaned_data['em']
            QQ = sf.cleaned_data['QQ']
            intro = sf.cleaned_data['intro']
            # u = UserProfile.objects.filter(username=username)  # 为什么不能用filter
            u = UserProfile.objects.get(username=request.user.username)
            x = NewUser.objects.get(username=request.user.username)
            x.username = new_username  # ---------------两个表的账户名、邮箱同步更改---------------
            x.email = em
            x.save()
            # v = u(user=user, username=new_username, address=address, job=job, em=em,
            #       QQ=QQ, intro=intro)
            # v.save()
            u.user = request.user
            # u.password = request.password
            u.username = new_username
            u.address = address
            u.job = job
            u.em = em
            u.QQ = QQ
            u.intro = intro
            u.save()
            # print(u.intro)  # 测试
            return render(request, 'user.html', {'form': sf})
        else:
            # p = sf.errors  # 测试用、表单验证不通过返回错误信息
            p = '个人信息不能为空！'
            return render(request, 'setting.html', {'form': sf, 'msg': p})


@login_required  # -------------修改密码-----------------
def set_password(request):
    if request.method == 'POST':
        form = PassForm(request.POST)
        if form.is_valid():
            old_pd = form.cleaned_data['old_pd']
            new_pd = form.cleaned_data['new_pd']
            u = UserProfile.objects.get(username=request.user.username)
            x = NewUser.objects.get(username=request.user.username)
            if u.password == old_pd:
                if old_pd == new_pd:
                    return render(request, 'set_pd.html', {'form': form, 'msg2': '两次密码不能相同'})
                else:
                    u.password = new_pd
                    u.save()
                    x.set_password(new_pd)  # 设置密码加密，不然是明文，admin里密码显示也是明文，登录不了
                    x.save()
                    return render(request, 'set_pd.html', {'form': form, 'msg2': '修改成功'})
            else:
                return render(request, 'set_pd.html', {'form': form, 'msg2': '密码有误'})

        else:
            p = form.errors  # 测试用、表单验证不通过返回错误信息
            return render(request, 'set_pd.html', {'form': form, 'msg2': p})
    else:
        form = PassForm
        return render(request, 'set_pd.html', {'form': form})


@login_required  # -------------头像上传-----------------
def head_img(request):
    user = request.user
    User = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = HeadImgForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES["imagefile"]
            parser = ImageFile.Parser()
            for chunk in f.chunks():
                parser.feed(chunk)
            img = parser.close()
            User.head_img = img
            User.save()
    return render









