from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from courses.models import CourseTypes, Courses
from django.core.urlresolvers import reverse
import json
import requests
from bs4 import BeautifulSoup
import urllib2

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

def naukri(request):
    print "AKSHAY"
    url="http://www.naukri.com/java-android-django-python-developer-nodejs-ios-json-html-angularjs-sql-javascript-css-jobs-in-delhi-ncr"
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    #all_div=soup.find_all('span', class_='desig')
    #length = len(all_div)

    return HttpResponse(str(soup), content_type="application/json")

def scrapRentOHouse(request):
    print "AKSHAY"
    url="http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Residential-Plot&cityName=Gurgaon"
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    all_div=soup.find_all('div', class_='srpBlockListRow')
    #results = []
    final = []
    print "AKSHAY2"
    counter = 0
    for one_div in all_div:
        print str(counter)
        counter = counter + 1
        onclickString = str(one_div['onclick'])
        pra = onclickString.find('event')+8
        sub1 = onclickString[pra:]
        pra2 = sub1.find("'")
        sub2 = sub1[:pra2]
        detailsUrl = "http://www.magicbricks.com"+sub2

        try:
            pageDetails = urllib2.urlopen(detailsUrl)
            soupDetails = BeautifulSoup(pageDetails)
            mainString = soupDetails.find('title')

            #results.append(onclickString)
            final.append(str(mainString))
        except:
            final.append("ERROR IN THIS: " + detailsUrl)

    print "AKSHAY3"
    finalString = ""
    for oneF in final:
        finalString = finalString + "\n" + oneF

    # url="http://www.magicbricks.com/propertyDetails/3-BHK-1767-Sq-ft-Multistorey-Apartment-FOR-Sale-Sohna-in-Gurgaon&id=4d423230303931363830?from=search"
    # page = urllib2.urlopen(url)
    # soup = BeautifulSoup(page)
    # mainString = soup.find('title')

    return HttpResponse(str(finalString), content_type="application/json")

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
    if len(searchString) > 30:
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
