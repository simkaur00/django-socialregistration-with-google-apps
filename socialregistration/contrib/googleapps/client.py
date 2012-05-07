from openid.extensions import ax

from socialregistration.contrib.openid.client import OpenIDClient

class GoogleAppsClient(OpenIDClient):

    available_info = {
        'country': 'http://axschema.org/contact/country/home',
        'email': 'http://axschema.org/contact/email',
        'firstname': 'http://axschema.org/namePerson/first',
        'lastname': 'http://axschema.org/namePerson/last',
        'language': 'http://axschema.org/pref/language',
    }

    def get_redirect_url(self):
        auth_request = self.consumer.begin(self.endpoint_url)

        # Use the openid AX Extension to get the user's name, email, and country
        ax_request = ax.FetchRequest()
        requested_info = self.available_info.keys()

        for alias in requested_info:
            ax_request.add(ax.AttrInfo(self.available_info[alias], alias=alias, required=True))

        auth_request.addExtension(ax_request)

        redirect_url = auth_request.redirectURL(self.get_realm(),
            self.get_callback_url())

        return redirect_url

    def complete(self, GET, path):
        super(GoogleAppsClient, self).complete(GET, path)

        if self.is_valid:
            try:
                ax_response = ax.FetchResponse.fromSuccessResponse(self.result)
            except AttributeError:
                # This can happen if we actually have a FailureResponse instead of a
                # SuccessResponse object.  I don't totally understand how it's possible
                # because in that case, 'is_valid' should return false.  Nevertheless,
                # I can get this situation to occur if I try to reload the openid/callback
                # page.  Therefore, when it does happen, we should ignore it and just
                # complete the request.
                pass
            else:
                requested_info = self.available_info.keys()
                for alias, prop in [('country', 'country'),
                                    ('email','email'),
                                    ('firstname', 'first_name'),
                                    ('lastname', 'last_name'),
                                    ('language', 'language')]:
                    try:
                        setattr(self, prop, ax_response.get(self.available_info[alias]))
                    except KeyError:
                        # This information isn't available in the response.  The user may not have
                        # entered it or we may not have permission to access it.
                        # Either way, life goes on.
                        pass
