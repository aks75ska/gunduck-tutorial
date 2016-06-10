from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from courses.models import CourseTypes, Courses
from django.core.urlresolvers import reverse
import json

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
    courseType = get_object_or_404(CourseTypes, pk=course_type_id)
    return render(request, 'courses/results.html', {'courseType': courseType})

def join(request, course_type_id):
    p = get_object_or_404(CourseTypes, pk=course_type_id)
    try:
        selected_choice = p.courses_set.get(pk=request.POST['choice'])
    except (KeyError, Courses.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'courses/detail.html', {
            'courseType': p,
            'error_message': "You didn't select a course.",
        })
    else:
        selected_choice.joinees += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('courses:results', args=(p.id,)))
    # return HttpResponse("You're joining a course of this course type %s." % course_type_id)

def faceBookChatBot(request):
    print "YAHOOOOOO"
    print request
    if request.method == 'GET':
        try:
            if request.GET.get("hub.verify_token") == "mindsaw_should_get_verified":
                return request.GET.get("hub.challenge")
            else:
                return HttpResponse(json.dumps([{"v": "Hit made to webhook in get!", "status": True}]), content_type = "application/json")
        except Exception as e:
            return HttpResponse(json.dumps([{"v": str(e), "status": True}]), content_type = "application/json")
    else:
        return HttpResponse(json.dumps([{"v": "Hit made to webhook but not get!", "status": True}]), content_type = "application/json")


