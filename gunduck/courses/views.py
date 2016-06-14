from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from courses.models import CourseTypes, Courses
from django.core.urlresolvers import reverse
import json
import requests
import logging

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
    # print "YAHOOOOOO"
    # print request
    if request.method == 'GET':
        try:
            if request.GET['hub.verify_token'] == "mindsaw_should_get_verified":
                bytesE = request.GET['hub.challenge'].encode('utf-8')
                return HttpResponse(bytesE, content_type = "application/json")
            else:
                return HttpResponse(json.dumps([{"v": "Wrong token", "status": False}]), content_type = "application/json")
        except Exception as e:
            return HttpResponse(json.dumps([{"v": str(e), "status": False}]), content_type = "application/json")
    elif request.method == 'POST':
        try:
            if request.body:
                dataDictionary = json.loads(request.body)
                if dataDictionary['object'] == "page":
                    allEntries = dataDictionary['entry']
                    for oneEntry in allEntries:
                        pageId = oneEntry['id']
                        ReceiveTime = oneEntry['time']
                        allMessages = oneEntry['messaging']
                        for oneMessage in allMessages:
                            try:
                                messageObject = oneMessage['message']
                                messageType = 'message'
                            except:
                                messageObject = None
                            if messageObject == None:
                                try:
                                    messageObject = oneMessage['optin']
                                    messageType = 'optin'
                                except:
                                    messageObject = None
                            if messageObject == None:
                                try:
                                    messageObject = oneMessage['delivery']
                                    messageType = 'delivery'
                                except:
                                    messageObject = None
                            if messageObject == None:
                                try:
                                    messageObject = oneMessage['postback']
                                    messageType = 'postback'
                                except:
                                    messageObject = None
                            if messageObject == None:
                                messageType = 'None'
                            registerCall(oneMessage, messageType)
                    #return HttpResponse(json.dumps([{"v": "Msg Received", "status": True}]), content_type = "application/json")
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(json.dumps([{"v": "Response not from page", "status": False}]), content_type = "application/json")
            else:
                return HttpResponse(json.dumps([{"v": "Response body not found", "status": False}]), content_type = "application/json")
        except Exception as e:
            return HttpResponse(json.dumps([{"v": str(e), "status": False}]), content_type = "application/json")
    else:
        return HttpResponse(json.dumps([{"v": "No Get or Post", "status": False}]), content_type = "application/json")

def registerCall(oneMessage, messageType):
    if messageType == "message":
        print "MESSAGE RECEIVED"
        senderId = oneMessage['sender']['id']
        recepientPageId = oneMessage['recipient']['id']
        messageTime = oneMessage['timestamp']
        messageObject = oneMessage['message']
        msgMID = messageObject['mid']
        msgSEQ = messageObject['seq']
        try:
            msgTEXT = messageObject['text']
            searchResult = searchMovie(senderId, msgTEXT)
            if searchResult != "N":
                sendTextMessage(senderId, searchResult);
            else:
                pass
        except:
            msgTEXT = None
        if msgTEXT == None:
            try:
                msgTEXT = messageObject['attachments']
                sendTextMessage(senderId, "Message with attachment received");
            except:
                msgTEXT = None
                print "NO TEXT NO ATTACHMENT"
    else:
        print messageType+" Received"

def searchMovie(senderId, searchString):
    if len(searchString) > 20:
        return "Oops! Your search string is too long for me to process. Please enter a string with less than 20 characters :/"
    else:
        try:
            response = requests.post("http://www.omdbapi.com/?s="+searchString)
            dataDict = json.loads(response.content)
            if dataDict['Response'] == "False":
                return dataDict['Error']
            elif dataDict['Response'] == "True":
                posterURL = dataDict['Search'][0]['Poster']
                if posterURL == "N/A":
                    pass
                else:
                    sendImageMessage(senderId, posterURL)
                    return "N"
                return "total results found: "+dataDict['totalResults']
            else:
                return "Invalid Request"
        except Exception as e:
            print e
            return str(e)

def sendTextMessage(senderId, messageToSend):
    messageData = json.dumps({"recipient": {"id" : senderId}, "message": {"text" : messageToSend}})
    callSendAPI(messageData);

def sendImageMessage(senderId, imageURL):
    messageData = json.dumps({"recipient": {"id" : senderId}, "message": {"attachment" : {"type":"image",
      "payload":{
        "url": imageURL
      } } } })
    callSendAPI(messageData);

def callSendAPI(messageData):
    PAGE_ACCESS_TOKEN = "EAAB7yhcKATcBALT1NgyX6ZCoBpTSHOkc1iXdylk6TkZAUiZAo5aRdDjikQvQZAyQcDTdVGO1xwLIw2vdH7bUx9z9qUAnKZBycd2IRjFO6lsJmtZCPSWXJ1LTLnUDGJ1EkqoeCtOllFClPHMxeUkbUYP9UCVFY7EdMPhZCHre400jQZDZD"
    print "CALLING SEND API " + messageData
    try:
        response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token="+PAGE_ACCESS_TOKEN, data=messageData,
            headers = {"Content-Type": 'application/json'})
    except Exception as e:
        print e
