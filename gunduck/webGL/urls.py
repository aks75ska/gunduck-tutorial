from django.conf.urls import patterns, include, url
from django.contrib import admin
from webGL import views

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^tutorial1/$', views.tutorial1, name='tutorial1'),

)
