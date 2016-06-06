from django.conf.urls import patterns, include, url
from django.contrib import admin

# urlpatterns = [
#     # Examples:
#     # url(r'^$', 'gunduck.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),

#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^courses/' , include('courses.urls')),
# ]

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^courses/' , include('courses.urls')),

)
