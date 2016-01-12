# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0006_subjeffit_registration_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjeffit',
            name='registration_code',
        ),
        migrations.AddField(
            model_name='cohort',
            name='registration_code',
            field=models.CharField(default=b'351Q1W', max_length=6),
        ),
    ]
