from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the courses index.")

def detail(request, course_type_id):
    return HttpResponse("You're looking at course type %s." % course_type_id)

def results(request, course_type_id):
    response = "You're looking at the courses of the course type %s."
    return HttpResponse(response % course_type_id)

def join(request, course_type_id):
    return HttpResponse("You're joining a course of this course type %s." % course_type_id)

