from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from socialregistration.views import SetupCallback
from socialregistration.contrib.googleapps.client import GoogleAppsClient
from socialregistration.contrib.googleapps.models import GoogleAppsProfile
from socialregistration.contrib.openid.views import OpenIDCallback, OpenIDRedirect

class GoogleAppsRedirect(OpenIDRedirect):
    client = GoogleAppsClient

    def post(self, request):
        return self.get(request)

    def get(self, request):
        try:
            domain = request.REQUEST['domain']
        except:
            raise Exception('You must specify a domain to use with Google Apps')

        request.session['next'] = self.get_next(request)

        # We don't want to pass in the whole session object as this might not
        # be pickleable depending on what session backend one is using.
        # See issue #73 in django-socialregistration
        client = self.get_client()(dict(request.session.items()),
            'https://www.google.com/accounts/o8/site-xrds?ns=2&hd={}'.format(domain))

        request.session[self.get_client().get_session_key()] = client

        return HttpResponseRedirect(client.get_redirect_url())


class GoogleAppsCallback(OpenIDCallback):
    setup_view = 'socialregistration:googleapps:setup'

class GoogleAppsSetup(SetupCallback):
    template_name = 'socialregistration/openid/openid.html'
    profile = GoogleAppsProfile
    client = GoogleAppsClient

    def create_user(self, client=None):
        """
        Create and return a new user model.  If the google apps authentication process
        returned the user's first/last name and email, also add those to the user model.
        """
        new_user = User()

        for prop in ['first_name', 'last_name', 'email']:
            try:
                setattr(new_user, prop, getattr(client, prop))
            except AttributeError:
                pass
        return new_user

    def get_lookup_kwargs(self, request, client):
        return { 'identity': client.get_identity() }
