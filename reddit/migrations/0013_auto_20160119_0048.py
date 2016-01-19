# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0012_auto_20160112_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='reddituser',
            name='total_karma',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cohort',
            name='registration_code',
            field=models.CharField(default=b'S76SUD', max_length=6),
        ),
    ]
