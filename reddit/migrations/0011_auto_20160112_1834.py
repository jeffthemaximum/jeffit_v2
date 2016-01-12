# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0010_cohort_registration_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cohort',
            name='registration_code',
            field=models.CharField(default=b'WQ9RHA', max_length=6),
        ),
    ]
