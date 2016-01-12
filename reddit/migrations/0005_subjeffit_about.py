# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0004_auto_20160108_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjeffit',
            name='about',
            field=models.TextField(max_length=5000, blank=True),
        ),
    ]
