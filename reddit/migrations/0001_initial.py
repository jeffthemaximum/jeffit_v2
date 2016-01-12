# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author_name', models.CharField(max_length=12)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('ups', models.IntegerField(default=0)),
                ('downs', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('raw_comment', models.TextField(blank=True)),
                ('html_comment', models.TextField(blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RedditUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(default=None, max_length=35, null=True, blank=True)),
                ('last_name', models.CharField(default=None, max_length=35, null=True, blank=True)),
                ('email', models.EmailField(default=None, max_length=254, null=True, blank=True)),
                ('about_text', models.TextField(default=None, max_length=500, null=True, blank=True)),
                ('about_html', models.TextField(default=None, null=True, blank=True)),
                ('gravatar_hash', models.CharField(default=None, max_length=32, null=True, blank=True)),
                ('display_picture', models.NullBooleanField(default=False)),
                ('homepage', models.URLField(default=None, null=True, blank=True)),
                ('twitter', models.CharField(default=None, max_length=15, null=True, blank=True)),
                ('github', models.CharField(default=None, max_length=39, null=True, blank=True)),
                ('comment_karma', models.IntegerField(default=0)),
                ('link_karma', models.IntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subjeffit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author_name', models.CharField(max_length=12)),
                ('subjeffit_title', models.CharField(max_length=250)),
                ('title', models.CharField(max_length=250)),
                ('url', models.URLField(null=True, blank=True)),
                ('text', models.TextField(max_length=5000, blank=True)),
                ('text_html', models.TextField(blank=True)),
                ('ups', models.IntegerField(default=0)),
                ('downs', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment_count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(to='reddit.RedditUser')),
                ('subjeffit', models.ForeignKey(to='reddit.Subjeffit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote_object_id', models.PositiveIntegerField()),
                ('value', models.IntegerField(default=0)),
                ('submission', models.ForeignKey(to='reddit.Submission')),
                ('user', models.ForeignKey(to='reddit.RedditUser')),
                ('vote_object_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to='reddit.RedditUser'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', blank=True, to='reddit.Comment', null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='submission',
            field=models.ForeignKey(to='reddit.Submission'),
        ),
    ]
