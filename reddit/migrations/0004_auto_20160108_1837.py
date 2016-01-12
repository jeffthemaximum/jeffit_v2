# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0003_auto_20160108_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cohort',
            name='reddit_users',
            field=models.ManyToManyField(related_name='cohorts', to='reddit.RedditUser'),
        ),
    ]
