# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-05 07:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('com', '0016_auto_20161204_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keep',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
