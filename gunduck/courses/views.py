from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from courses.models import CourseTypes, Courses

# Create your views here.
def index(request):
    course_type_list = CourseTypes.objects.order_by('-created_time')[:10]
    template = loader.get_template('courses/index.html')
    context = {
        'course_type_list': course_type_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, course_type_id):
    return HttpResponse("You're looking at course type %s." % course_type_id)

def results(request, course_type_id):
    response = "You're looking at the courses of the course type %s."
    return HttpResponse(response % course_type_id)

def join(request, course_type_id):
    return HttpResponse("You're joining a course of this course type %s." % course_type_id)

