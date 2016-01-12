# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0009_remove_cohort_registration_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='cohort',
            name='registration_code',
            field=models.CharField(default=b'ZWXY5C', max_length=6),
        ),
    ]
