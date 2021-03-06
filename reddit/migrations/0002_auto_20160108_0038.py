# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=70)),
            ],
        ),
        migrations.AddField(
            model_name='reddituser',
            name='instructor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reddituser',
            name='cohort',
            field=models.ForeignKey(default=0, to='reddit.Cohort'),
            preserve_default=False,
        ),
    ]
