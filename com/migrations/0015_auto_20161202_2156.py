# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-02 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('com', '0014_auto_20161202_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='intro',
            field=models.TextField(blank=True, max_length=256, null=True, verbose_name='intro'),
        ),
    ]
