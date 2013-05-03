from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils import importlib
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateResponseMixin
from socialregistration import signals
from socialregistration.settings import SESSION_KEY
import urlparse

ERROR_VIEW = getattr(settings, 'SOCIALREGISTRATION_ERROR_VIEW_FUNCTION',
    None)

class CommonMixin(TemplateResponseMixin):
    """
    Provides default functionality used such as authenticating and signing
    in users, redirecting etc.
    """

    def import_attribute(self, path):
        """
        Import an attribute from a module.
        """
        module = '.'.join(path.split('.')[:-1])
        function = path.split('.')[-1]

        module = importlib.import_module(module)
        return getattr(module, function)

    def get_next(self, request):
        """
        Returns a url to redirect to after the login / signup.
        """
        if 'next' in request.session: 
            next = request.session['next']
            del request.session['next']
        elif 'next' in request.GET:
            next = request.GET.get('next')
        elif 'next' in request.POST:
            next = request.POST.get('next')
        else:
            next = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
        
        netloc = urlparse.urlparse(next)[1]
        
        if netloc and netloc != request.get_host():
            next = getattr(settings, 'LOGIN_REDIRECT_URL', '/')

        return next

    def set_next(self, request, next_url):
        """
        Sets the url to redirect to after the login / signup.
        """
        request.session['next'] = next_url

    def authenticate(self, **kwargs):
        """
        Authenticate a user against all configured authentication backends.
        """
        return authenticate(**kwargs)

    def login(self, request, user):
        """
        Sign a user in.
        """
        return login(request, user)

    def inactive_response(self, request):
        """
        Return an inactive message.
        """
        inactive_url = getattr(settings, 'LOGIN_INACTIVE_REDIRECT_URL', '')
        if inactive_url:
            return HttpResponseRedirect(inactive_url)
        else:
            return self.error_to_response(request, {'error': _("This user account is marked as inactive.")})

    def redirect(self, request):
        """
        Redirect the user back to the ``next`` session/request variable.
        """
        return HttpResponseRedirect(self.get_next(request))

class ClientMixin(object):
    """
    Views such as ``OAuthRedirectView`` require a client to work with. This is
    the interface to it.

    """
    #: The client class we'll be working with
    client = None

    def get_client(self):
        """
        Return the client class or raise an ``AttributeError`` if
        ``self.client`` is not set.
        """
        if self.client is None:
            raise AttributeError('`self.client` is `None`')
        return self.client

class ProfileMixin(object):
    """
    Views such as ``SetupCallback`` require a profile model to work with. This is
    the interface to it.

    """
    #: The profile model that we'll be working with
    profile = None

    def get_lookup_kwargs(self, request, client):
        """
        Return a dictionary to look up a profile object.
        """
        raise NotImplementedError

    def get_model(self):
        """
        Return the profile model or raise an ``AttributeError``
        if ``self.profile`` is not set.
        """
        if self.profile is None:
            raise AttributeError('`self.profile` is `None`')
        return self.profile

    def create_user(self, client=None):
        """
        Create and return an empty user model.
        """
        return User()

    def create_profile(self, user, save=False, client=None, **kwargs):
        """
        Create a profile model.

        :param user: A user object
        :param save: If this is set, the profile will
            be saved to DB straight away
        :param client: This is the authentication client that was used
            for the log-in request
        :type save: bool
        """
        profile, created = self.get_or_create_profile(user, save, client, **kwargs)
        return profile

    def get_profile(self, **kwargs):
        """
        Return a profile object
        """
        return self.get_model().objects.get(**kwargs)

    def get_or_create_profile(self, user, save=False, client=None, **kwargs):
        """
        Return a profile from DB or if there is none, create a new one.

        :param user: A user object
        :param save: If set, a new profile will be saved.
        :param client: This is the authentication client that was used
            for the log-in request
        :type save: bool
        """
        props_to_set = client.get_profile_properties() if client is not None else {}
        created = False
        needs_saved = False
        profile = None

        try:
            profile = self.get_model().objects.get(user=user, **kwargs)
        except self.get_model().DoesNotExist:
            profile = self.get_model()(user=user, **kwargs)
            needs_saved = True

        for prop in props_to_set.keys():
            if props_to_set[prop] != getattr(profile, prop):
                setattr(profile, prop, props_to_set[prop])
                needs_saved = True

        if save and needs_saved:
            profile.save()

        return profile, created

class SessionMixin(object):
    """
    When a new user is signing up the user and profile models and api client
    need to be carried accross two views via session. This mixin handles
    storage, retrieval and cleanup of said values.
    """

    def store_profile(self, request, profile):
        """
        Store the profile data to the session
        """
        request.session['%sprofile' % SESSION_KEY] = profile

    def store_user(self, request, user):
        """
        Store the user data to the session
        """
        request.session['%suser' % SESSION_KEY] = user

    def store_client(self, request, client):
        """
        Store the client to the session
        """
        request.session['%sclient' % SESSION_KEY] = client

    def get_session_data(self, request):
        """
        Return a tuple ``(user, profile, client)`` from the session.
        """
        user = request.session['%suser' % SESSION_KEY]
        profile = request.session['%sprofile' % SESSION_KEY]
        client = request.session['%sclient' % SESSION_KEY]
        return user, profile, client

    def delete_session_data(self, request):
        """
        Clear all session data.
        """
        for key in ['user', 'profile', 'client']:
            try: del request.session['%s%s' % (SESSION_KEY, key)]
            except KeyError: pass


class SignalMixin(object):
    """
    When signing users up or signing users in we need to send out signals to
    notify other parts of the code. This mixin provides an interface for sending
    the signals.
    """
    def send_login_signal(self, request, user, profile, client):
        """
        Send a signal that a user logged in. This signal should be sent only if
        the user was *not* logged into Django.
        """
        signals.login.send(sender=profile.__class__, user=user,
            profile=profile, client=client, request=request)

    def send_connect_signal(self, request, user, profile, client):
        """
        Send a signal that a user connected a social profile to his Django
        account. This signal should be sent *only* when the a new social
        connection was created.
        """
        signals.connect.send(sender=profile.__class__, user=user, profile=profile,
            client=client, request=request)

class ErrorMixin(object):
    def error_to_response(self, request, error_dict, **context):
        if ERROR_VIEW:
            return self.import_attribute(ERROR_VIEW)(request, error_dict, **context)
        return self.render_to_response(error_dict, **context)

class SocialRegistration(CommonMixin, ClientMixin, ProfileMixin, SessionMixin,
    SignalMixin, ErrorMixin):
    """
    Combine all mixins into a single class.
    """
    pass
