from django.db import models
import datetime
from time import time

# Create your models here.

class CourseTypes(models.Model):
    course_type_name = models.CharField(max_length=50)
    course_type_description = models.CharField(max_length=500)
    created_time = models.DateTimeField('date and time of creation')

    def __unicode__(self):
        return str(self.course_type_name)

    def was_published_recently(self):
        now = datetime.datetime.now()
        return datetime.datetime.now() - datetime.timedelta(days=1) <= self.created_time <= datetime.datetime.now()
    was_published_recently.admin_order_field = 'created_time'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Courses(models.Model):
    course_name = models.CharField(max_length=50)
    course_description = models.CharField(max_length=500)
    course_type = models.ForeignKey(CourseTypes)
    created_time = models.DateTimeField('date and time of creation')
    joinees = models.BigIntegerField(default=0)

    def __unicode__(self):
        return str(self.course_name)

def get_upload_file_name(instance, filename):
    return "uploaded_files/courses_images/%s_%s" %(filename.replace(' ','_'), str(time()).replace('.','_'))

class ImageLocker(models.Model):
    name = models.CharField(max_length=255)
    photo = models.FileField(upload_to=get_upload_file_name)

    def __unicode__(self):
        return str(self.name)

