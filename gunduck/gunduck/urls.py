from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# urlpatterns = [
#     # Examples:
#     # url(r'^$', 'gunduck.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),

#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^courses/' , include('courses.urls')),
# ]

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^courses/' , include('courses.urls', namespace="courses")),

    url(r'^$', 'gunduck.views.homePage'),

)+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
