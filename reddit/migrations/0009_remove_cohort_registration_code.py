# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0008_auto_20160112_0112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cohort',
            name='registration_code',
        ),
    ]
