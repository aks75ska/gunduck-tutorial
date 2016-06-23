from django.conf.urls import patterns, include, url
from django.contrib import admin
from courses import views

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^(?P<course_type_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<course_type_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<course_type_id>[0-9]+)/join/$', views.join, name='join'),

    url(r'^chatbots/facebook/webhook/$', views.faceBookChatBot, name='faceBookChatBot'),
    url(r'^scrapper/rentOHouse/$', views.scrapRentOHouse, name='scrapRentOHouse'),
    url(r'^scrapper/naukri/$', views.naukri, name='naukri'),

)
