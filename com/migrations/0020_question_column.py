# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-13 02:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('com', '0019_auto_20161212_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='com.Column', verbose_name='belong to'),
        ),
    ]
