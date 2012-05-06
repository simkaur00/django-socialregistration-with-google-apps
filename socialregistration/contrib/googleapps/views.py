from socialregistration.contrib.googleapps.client import GoogleAppsClient
from socialregistration.contrib.openid.views import OpenIDRedirect, OpenIDSetup

class GoogleAppsRedirect(OpenIDRedirect):
    client = GoogleAppsClient

    def post(self, request, domain):
        return self.get(request, domain)

    def get(self, request, domain):
        request.session['next'] = self.get_next(request)

        # We don't want to pass in the whole session object as this might not
        # be pickleable depending on what session backend one is using.
        # See issue #73 in django-socialregistration
        client = self.get_client()(dict(request.session.items()),
            'https://www.google.com/accounts/o8/site-xrds?ns=2&hd={}'.format(domain))
            #'https://www.google.com/accounts/o8/.well-known/host-meta?hd={}'.format(domain))

        request.session[self.get_client().get_session_key()] = client

        return HttpResponseRedirect(client.get_redirect_url())

class GoogleAppsSetup(OpenIDSetup):
    pass
