# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=150)),
                ('body', models.TextField()),
                ('at', models.DateTimeField(default=datetime.datetime.now)),
                ('bounced', models.BooleanField(default=False)),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'emails',
            },
        ),
        migrations.CreateModel(
            name='MailoutCategory',
            fields=[
                ('key', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('default', models.BooleanField()),
                ('title', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='MailoutUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emails.MailoutCategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
