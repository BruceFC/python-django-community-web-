# import datetime
from django.db import models
from django.contrib.auth.models import User
# from django.utils.encoding import python_2_unicode_compatible
# from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# @python_2_unicode_compatible
class NewUser(AbstractUser):
    profile = models.CharField('profile', default='', max_length=256)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(NewUser, unique=True, verbose_name='用户额外信息')
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    head_img = models.ImageField(upload_to='profile_images', blank=True, null=True)
    address = models.CharField('address', max_length=100, blank=True, null=True)
    job = models.CharField('job', max_length=100, blank=True, null=True)
    em = models.CharField('em', max_length=50, blank=True, null=True)
    QQ = models.CharField('QQ', max_length=50, blank=True, null=True)
    intro = models.TextField('intro', max_length=256, blank=True, null=True)
    # keep = models.ForeignKey('Keep', blank=True, null=True)  # 用户个人收藏信息 不这样写
    keep_num = models.IntegerField(default=0)  # 收藏问题数
    answered_num = models.IntegerField(default=0)  # 回答数
    quized_num = models.IntegerField(default=0)  # 提问数


# Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username


# @python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField('column_name', max_length=256)
    intro = models.TextField('introduction', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'column'
        verbose_name_plural = 'column'
        ordering = ['name']


class QuestionManager(models.Manager):
    def query_by_column(self, column_id):
        query = self.get_queryset().filter(column_id=column_id)
        return query

    def query_by_user(self, user_id):
        user = User.objects.get(id=user_id)
        question_list = user.question_set.all()
        return question_list

    # def query_by_polls(self):
    #     query = self.get_queryset().order_by('poll_num')
    #     return query

    def query_by_time(self):
        query = self.get_queryset().order_by('-pub_date')
        return query

    def query_by_keyword(self, keyword):
        query = self.get_queryset().filter(title__contains=keyword)
        return query


# @python_2_unicode_compatible
class Question(models.Model):
    column = models.ForeignKey(Column, blank=True, null=True, verbose_name='belong to')
    title = models.CharField(max_length=256)
    content = models.TextField('content')     # 命名待改进
    questioner = models.ForeignKey('Questioner')
    # questioner = models.ForeignKey('NewUser', null=True)    # 改！
    user = models.ManyToManyField('NewUser', blank=True)   # 普通用户、路人
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
# update_time = models.DateTimeField(auto_now=True, null=True)
# published = models.BooleanField('notDraft', default=True)
#     poll_num = models.IntegerField(default=0)  # 用不到
    answer_num = models.IntegerField(default=0)  # 回答数
    keep_num = models.IntegerField(default=0)  # 收藏数
    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'question'
        verbose_name_plural = 'question'


class Answer(models.Model):  # -------------------回答-------------------
    user = models.ForeignKey('NewUser', null=True)  # 回答的人是普通用户，路人
    question = models.ForeignKey(Question, null=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    poll_num = models.IntegerField(default=0)

    def __str__(self):
        return self.content


class Questioner(models.Model):
    name = models.CharField(max_length=256)
    profile = models.CharField('profile', default='', max_length=256)
    password = models.CharField('password', max_length=256)
    register_date = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.name


class Poll(models.Model):           # -------------------给回答点赞-----------------------
    user = models.ForeignKey('NewUser', null=True)
    # question = models.ForeignKey('Question', null=True)
    answer = models.ForeignKey('Answer', null=True)
    # poll_time = models.DateTimeField(auto_now_add=True, editable=True)


# class KeepManager(models.Manager):  # -------------------收藏manager----------------
#     def query_by_keeper(self, user_id):
#         user = NewUser.objects.get(id=user_id)
#         keep_list = user.keep_set.all()
#         return keep_list


class Keep(models.Model):       # -----------------------收藏问题---------------------------
    user = models.ForeignKey('NewUser', null=True)
    question = models.ForeignKey(Question, null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=True)
    # objects = KeepManager()


class Quiz(models.Model):       # -----------------------收藏问题---------------------------
    user = models.ForeignKey('NewUser', null=True)
    question = models.ForeignKey(Question, null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=True)
    # objects = KeepManager()


# class Concern(models.Model):  # ---------------------关注人----------------------
#     user = models.ForeignKey('NewUser', null=True)
#     concerned_user = models.ForeignKey('NewUser', null=True)
#     concern_time = models.DateTimeField(auto_now_add=True)
#     # objects = KeepManager()



