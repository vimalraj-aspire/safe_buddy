# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-07 10:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160907_1019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friend',
            old_name='friend',
            new_name='friend_profile',
        ),
        migrations.RenameField(
            model_name='friend',
            old_name='user',
            new_name='user_profile',
        ),
    ]