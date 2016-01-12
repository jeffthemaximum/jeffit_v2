# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0011_auto_20160112_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cohort',
            name='reddit_users',
            field=models.ManyToManyField(default=None, related_name='cohorts', to='reddit.RedditUser', blank=True),
        ),
        migrations.AlterField(
            model_name='cohort',
            name='registration_code',
            field=models.CharField(default=b'LNNI9G', max_length=6),
        ),
    ]
