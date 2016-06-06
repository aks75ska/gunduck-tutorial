from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from courses.models import CourseTypes, Courses

# Create your views here.
def index(request):
    course_type_list = CourseTypes.objects.order_by('-created_time')[:10]
    context = {
        'course_type_list': course_type_list,
    }
    return render(request, 'courses/index.html', context)

def detail(request, course_type_id):
    courseType = get_object_or_404(CourseTypes, pk=course_type_id)
    return render(request, 'courses/detail.html', {'courseType': courseType})

def results(request, course_type_id):
    response = "You're looking at the courses of the course type %s."
    return HttpResponse(response % course_type_id)

def join(request, course_type_id):
    return HttpResponse("You're joining a course of this course type %s." % course_type_id)

