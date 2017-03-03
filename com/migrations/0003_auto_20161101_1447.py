# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-01 06:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('com', '0002_auto_20161101_1443'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'title', 'verbose_name_plural': 'title'},
        ),
        migrations.RemoveField(
            model_name='question',
            name='describe',
        ),
        migrations.AddField(
            model_name='question',
            name='content',
            field=models.TextField(default=django.utils.timezone.now, verbose_name='content'),
            preserve_default=False,
        ),
    ]
