from django.contrib import admin
# from django.db import models
# from django import forms
from .models import Answer, Question, Column, NewUser, Questioner, UserProfile, Keep, Quiz
# from com.models import UserProfile  # 导入user类


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'question_id', 'pub_date', 'content', 'poll_num')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'keep_num')


class NewUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined', 'profile')


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'intro')


class QuestionerAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'head_img')  # 加


class KeepAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'question_id', 'created_on')  # 加


class QuizAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'question_id', 'created_on')  # 加


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Questioner, QuestionerAdmin)
admin.site.register(UserProfile, UserProfileAdmin)  # 加
admin.site.register(Keep, KeepAdmin)  # 加
admin.site.register(Quiz, QuizAdmin)  # 加