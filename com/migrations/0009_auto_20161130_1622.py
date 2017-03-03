# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-30 08:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('com', '0008_remove_question_column'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='Intro',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='个人简介'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='QQ',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='QQ'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='居住地'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='answered_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='collected',
            field=models.ManyToManyField(blank=True, to='com.Question'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='concerned_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='em',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='邮箱'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='job',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='工作'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户额外信息'),
        ),
    ]
