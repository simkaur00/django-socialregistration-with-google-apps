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
        #self.result = self.consumer.complete(GET, urlparse.urljoin(self.get_realm(),
        #    path))
        if self.is_valid:
            print '\n\n'
            ax_response = ax.FetchResponse.fromSuccessResponse(self.result)
            requested_info = self.available_info.keys()
            for alias, prop in [('country', 'country'),
                                ('email','email'),
                                ('firstname', 'first_name'),
                                ('lastname', 'last_name'),
                                ('language', 'language')]:
                setattr(self, prop) = ax_response.get(self.available_info[alias])
                print '\n'
                print '{} = {}'.format(prop, getattr(self, prop))
            print '\n\n\n'
