# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0007_auto_20160109_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cohort',
            name='registration_code',
            field=models.CharField(default=b'MC547M', max_length=6),
        ),
    ]
