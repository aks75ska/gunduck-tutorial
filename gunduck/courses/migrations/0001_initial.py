# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_name', models.CharField(max_length=50)),
                ('course_description', models.CharField(max_length=500)),
                ('created_time', models.DateTimeField(verbose_name=b'date and time of creation')),
            ],
        ),
        migrations.CreateModel(
            name='CourseTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_type_name', models.CharField(max_length=50)),
                ('course_type_description', models.CharField(max_length=500)),
                ('created_time', models.DateTimeField(verbose_name=b'date and time of creation')),
            ],
        ),
        migrations.AddField(
            model_name='courses',
            name='course_type',
            field=models.ForeignKey(to='courses.CourseTypes'),
        ),
    ]
