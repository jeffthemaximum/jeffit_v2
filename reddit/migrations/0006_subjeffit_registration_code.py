# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0005_subjeffit_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjeffit',
            name='registration_code',
            field=models.CharField(default=b'BD9YOI', max_length=6),
        ),
    ]
