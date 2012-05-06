from django.conf import settings
from django.conf.urls.defaults import *
from socialregistration.contrib.googleapps.views import GoogleAppsRedirect, \
    GoogleAppsSetup
from socialregistration.contrib.openid.views import OpenIDCallback

urlpatterns = patterns('',
    url('^redirect/$', GoogleAppsRedirect.as_view(), name='redirect'),
    url('^callback/$', OpenIDCallback.as_view(), name='callback'),
    url('^setup/$', GoogleAppsSetup.as_view(), name='setup'),
)
