from django.conf import settings
from socialregistration.compat.urls import *
from socialregistration.views import Logout, Setup

urlpatterns = patterns('',)

if 'socialregistration.contrib.openid' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^openid/', include('socialregistration.contrib.openid.urls',
            namespace='openid')))

if 'socialregistration.contrib.googleapps' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^googleapps/', include('socialregistration.contrib.googleapps.urls',
            namespace='googleapps')))

if 'socialregistration.contrib.twitter' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^twitter/', include('socialregistration.contrib.twitter.urls',
            namespace='twitter')))

if 'socialregistration.contrib.linkedin' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^linkedin/', include('socialregistration.contrib.linkedin.urls',
            namespace='linkedin')))

if 'socialregistration.contrib.facebook' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^facebook/', include('socialregistration.contrib.facebook.urls',
            namespace='facebook')))

if 'socialregistration.contrib.github' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^github/', include('socialregistration.contrib.github.urls',
            namespace='github')))

if 'socialregistration.contrib.foursquare' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^foursquare/', include('socialregistration.contrib.foursquare.urls',
            namespace='foursquare')))

if 'socialregistration.contrib.tumblr' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^tumblr/', include('socialregistration.contrib.tumblr.urls',
            namespace='tumblr')))
    
if 'socialregistration.contrib.instagram' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^instagram/', include('socialregistration.contrib.instagram.urls',
            namespace='instagram')))

if 'socialregistration.contrib.google' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^google/', include('socialregistration.contrib.google.urls',
            namespace='google')))

urlpatterns = urlpatterns + patterns('',
    url(r'^setup/$', Setup.as_view(), name='setup'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
)


