# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import courses.models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_courses_joinees'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageLocker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('photo', models.FileField(upload_to=courses.models.get_upload_file_name)),
            ],
        ),
    ]
