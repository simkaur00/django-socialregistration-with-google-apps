from django.conf import settings
from django.conf.urls.defaults import *
from socialregistration.contrib.googleapps.views import GoogleAppsRedirect, \
    GoogleAppsSetup, GoogleAppsCallback

urlpatterns = patterns('',
    url('^redirect/$', GoogleAppsRedirect.as_view(), name='redirect'),
    url('^callback/$', GoogleAppsCallback.as_view(), name='callback'),
    url('^setup/$', GoogleAppsSetup.as_view(), name='setup'),
)
