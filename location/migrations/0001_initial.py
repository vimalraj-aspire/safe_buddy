# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-07 14:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0005_auto_20160907_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=8)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=8)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('user_profile', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userprofileLocation', to='users.UserProfile')),
            ],
        ),
    ]