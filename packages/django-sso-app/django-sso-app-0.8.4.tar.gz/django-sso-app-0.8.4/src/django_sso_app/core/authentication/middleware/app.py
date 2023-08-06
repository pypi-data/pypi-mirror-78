import logging
# import inspect

from django.contrib import auth
from django.urls import reverse
from django.conf import settings

from ...permissions import is_authenticated
from ...exceptions import ServiceSubscriptionRequiredException, ProfileIncompleteException
from ...utils import check_user_can_login, set_session_key, get_session_key
from ... import app_settings

from .base import DjangoSsoAppAuthenticationBaseMiddleware

logger = logging.getLogger('django_sso_app.core.middleware')

ADMIN_URL = '/{}'.format(settings.ADMIN_URL)
SSO_ID_JWT_KEY = 'sso_id'
PROFILE_INCOMPLETE_ENABLED_PATHS = [
    reverse('javascript-catalog'),
    reverse('profile.complete'),
]


class DjangoSsoAppAuthenticationAppMiddleware(DjangoSsoAppAuthenticationBaseMiddleware):

    def app_process_request(self, request, request_jwt, decoded_jwt):
        user = getattr(request, 'user', None)

        if not is_authenticated(user):
            # We are seeing this user for the first time in this session, attempt
            # to authenticate the user.
            try:
                if app_settings.APIGATEWAY_ENABLED:
                    consumer_username = get_session_key(request, '__dssoa__apigateway__consumer_username')

                    user = auth.authenticate(request=request,
                                             consumer_username=consumer_username,
                                             encoded_jwt=request_jwt,
                                             decoded_jwt=decoded_jwt)
                else:
                    user = auth.authenticate(request=request,
                                             encoded_jwt=request_jwt,
                                             decoded_jwt=decoded_jwt)

            except ServiceSubscriptionRequiredException as e:
                logger.debug('ServiceSubscriptionRequiredException. Redirecting to service subscription')

                set_session_key(request, '__dssoa__redirect', e.response)

            except ProfileIncompleteException as e:
                logger.debug('ProfileIncompleteException. Redirecting to profile completion')

                set_session_key(request, '__dssoa__redirect', e.response)

            except Exception as e:
                logger.exception('App middleware exception "{}"'.format(e))

                self._remove_invalid_user(request)

                return

            else:
                logger.info('User "{}" authenticated successfully!'.format(user))

                # set request user
                setattr(request, 'user', user)  # !!

        # further checks
        if is_authenticated(user):
            set_session_key(request, '__dssoa__requesting_user', user)

    # response
    def app_process_response(self, request, response):

        redirect = get_session_key(request, '__dssoa__redirect', None)

        if redirect is not None:
            return redirect

        # redirect to profile complete (if required)
        if get_session_key(request, '__dssoa__must_update_profile', False):
            requesting_user = get_session_key(request, '__dssoa__requesting_user')

            logger.info('Redirecting user "{}" to profile completion'.format(requesting_user))

            response = self._redirect_to_profile_complete_response(request.user)

        return response
