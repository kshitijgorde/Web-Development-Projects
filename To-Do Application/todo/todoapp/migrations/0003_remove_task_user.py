# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-29 02:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0002_task_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='user',
        ),
    ]