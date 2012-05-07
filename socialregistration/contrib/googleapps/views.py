from django.contrib.auth.models import User
from socialregistration.views import SetupCallback
from socialregistration.contrib.googleapps.client import GoogleAppsClient
from socialregistration.contrib.openid.views import OpenIDRedirect

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

class GoogleAppsSetup(SetupCallback):
    template_name = 'socialregistration/openid/openid.html'
    profile = GoogleAppsProfile
    client = GoogleAppsClient

    def create_user(self, client=None):
        # I think I need to include a client here or else I won't be able to look up
        # information from it.

        """
        Create and return a new user model.  If the google apps authentication process
        returned the user's first/last name and email, also add those to the user model.
        """
        new_user = User()

        for prop in ['first_name', 'last_name', 'email']:
            try:
                setattr(new_user, kw, getattr(client, kw))
            except AttributeError:
                pass
        return new_user

    def get_lookup_kwargs(self, request, client):
        kwargs_dict = { 'identity': client.get_identity() }

        for kw in ['country', 'language']:
            try:
                kwargs_dict[kw] = getattr(client, kw)
            except AttributeError:
                pass

        return kwargs_dict
