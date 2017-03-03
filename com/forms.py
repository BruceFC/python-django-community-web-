from django import forms
from .models import User, Question
# import datetime
# import re
# import markdown2


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': '用户名'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'placeholder': '密码'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label='username',
                               max_length=50,
                               widget=forms.TextInput(attrs={'id': 'username',
                                                             'onclick': 'authentication()'}))
    # email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class AnswerForm(forms.Form):
    # answer_content = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': '6'}))
    answer_content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'answer_content'
    }))


class SearchForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput)


class QuizForm(forms.Form):
    title = forms.CharField(
        # max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'question_title',
                'id': 'question_title'
            }
        )
    )
    content = forms.CharField(
        # min_length=1,
        widget=forms.Textarea(
            attrs={
                'class': 'question_content',
                'id': 'question_content'
            }
        )
    )


class SetInfoForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    address = forms.CharField(widget=forms.TextInput)
    job = forms.CharField(widget=forms.TextInput)
    em = forms.CharField(widget=forms.TextInput)
    QQ = forms.CharField(widget=forms.TextInput)
    intro = forms.CharField(widget=forms.Textarea)


class PassForm(forms.Form):
    old_pd = forms.CharField(widget=forms.PasswordInput)
    new_pd = forms.CharField(widget=forms.PasswordInput)


class HeadImgForm(forms.Form):
    head_img = forms.ImageField(required=False)
