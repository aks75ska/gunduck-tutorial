from django.contrib import admin

# Register your models here.

from .models import CourseTypes, Courses, ImageLocker

class CoursesInline(admin.TabularInline):
    model = Courses
    extra = 3

class CourseTypesAdmin(admin.ModelAdmin):
    fields = ['course_type_name', 'course_type_description', 'created_time']
    list_display = ('course_type_name', 'course_type_description', 'created_time', 'was_published_recently')
    list_filter = ['created_time']
    search_fields = ['course_type_name']
    inlines = [CoursesInline]

class ImageLockerAdmin(admin.ModelAdmin):
    fields = ['name', 'photo']
    list_display = ('name', 'photo')
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(CourseTypes, CourseTypesAdmin)
admin.site.register(ImageLocker, ImageLockerAdmin)
