from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
import json
import requests
from bs4 import BeautifulSoup
import urllib2

# Create your views here.

def tutorial1(request):
    return render_to_response('webGL/tutorial1.html')
