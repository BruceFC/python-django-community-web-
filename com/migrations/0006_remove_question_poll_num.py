# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-15 10:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('com', '0005_auto_20161114_2053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='poll_num',
        ),
    ]
