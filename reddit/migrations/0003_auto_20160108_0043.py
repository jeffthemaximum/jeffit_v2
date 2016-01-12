# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0002_auto_20160108_0038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reddituser',
            old_name='instructor',
            new_name='is_instructor',
        ),
        migrations.RemoveField(
            model_name='reddituser',
            name='cohort',
        ),
        migrations.AddField(
            model_name='cohort',
            name='reddit_users',
            field=models.ManyToManyField(to='reddit.RedditUser'),
        ),
    ]
