from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth import authenticate

from socialregistration.contrib.openid.models import OpenIDProfile

class GoogleAppsProfile(OpenIDProfile):
    country = models.CharField(max_length=3)
    language = models.CharField(max_length=6)

    def __unicode__(self):
        try:
            return 'Google Apps profile for %s' % (self.user)
        except User.DoesNotExist:
            return 'OpenID profile for None, via provider None'
