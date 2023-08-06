import logging

from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin  # https://stackoverflow.com/questions/42232606/django
                                                      # -exception-middleware-typeerror-object-takes-no-parameters

from ...permissions import is_authenticated, is_django_staff
from ...utils import set_session_key
from ... import app_settings

logger = logging.getLogger('django_sso_app.core.middleware')


PROFILE_INCOMPLETE_ENABLED_PATHS = [
    reverse('javascript-catalog'),
    reverse('profile.complete'),
]

class DjangoSsoAppAuthenticationBaseMiddleware(MiddlewareMixin):
    """
    See django.contrib.auth.middleware.RemoteUserMiddleware.
    """

    # Name of request header to grab username from.  This will be the key as
    # used in the request.META dictionary, i.e. the normalization of headers to
    # all uppercase and the addition of "HTTP_" prefix apply.
    header = app_settings.APIGATEWAY_CONSUMER_USERNAME_HEADER
    # Username for anonymous user
    anonymous_username = app_settings.APIGATEWAY_ANONYMOUS_CONSUMER_USERNAME

    @staticmethod
    def _clear_response_jwt(request):
        set_session_key(request, '__dssoa__clear_response_jwt', True)

    @staticmethod
    def _remove_invalid_user(request):
        """
        Removes the current authenticated user in the request which is invalid.
        """

        if is_authenticated(request.user):
            logger.info('removing invalid user "{}"'.format(request.user))

            auth.logout(request)

    @staticmethod
    def _redirect_to_profile_complete_response(user):
        _url = '{}'.format(app_settings.PROFILE_COMPLETE_URL)

        logger.info('User {} must complete profile,'
                    ' redirecting to {} ...'
                    .format(user, _url))

        response = HttpResponseRedirect(redirect_to=_url)

        return response

    @staticmethod
    def _request_path_is_disabled_for_incomplete_users(request_path):
        return (request_path not in PROFILE_INCOMPLETE_ENABLED_PATHS) and \
                not (request_path.startswith('/api/v1/')) and \
                not (request_path.startswith('/static/')) and \
                not (request_path.startswith('/media/')) and \
                not (request_path.startswith('/logout/')) and \
                not (request_path.startswith('/password/reset/')) and \
                not (request_path.startswith('/confirm-email/'))

    def process_request(self, request):
        raise NotImplementedError('process_request')

    def process_response(self, request, response):
        raise NotImplementedError('process_response')
