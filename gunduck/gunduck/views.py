from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.contrib import auth
import json
from django.contrib.auth.models import User, Group
from django.db.models import Max
import datetime
from gunduck.settings import DEBUG
from django.core.exceptions import ObjectDoesNotExist
import requests
from django.template import RequestContext

def homePage(request):
    return render_to_response('userViews/index.html')
