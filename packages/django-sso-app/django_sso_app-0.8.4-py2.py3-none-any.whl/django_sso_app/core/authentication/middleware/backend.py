import logging

from django.contrib import auth
from django.conf import settings

from ...permissions import is_authenticated
from ...exceptions import ProfileIncompleteException
from ...utils import check_user_can_login, set_session_key, get_session_key, invalidate_cookie
from ... import app_settings

from .base import DjangoSsoAppAuthenticationBaseMiddleware

logger = logging.getLogger('django_sso_app.core.middleware')

ADMIN_URL = '/{}'.format(settings.ADMIN_URL)
SSO_ID_JWT_KEY = 'sso_id'


class DjangoSsoAppAuthenticationBackendMiddleware(DjangoSsoAppAuthenticationBaseMiddleware):

    def backend_process_request(self, request, request_jwt, decoded_jwt):
        user = getattr(request, 'user', None)

        if not is_authenticated(request.user):
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

            except Exception as e:
                logger.exception('Backend middleware exception "{}"'.format(e))

                self._remove_invalid_user(request)

                return

            else:
                logger.info('User "{}" authenticated successfully!'.format(user))

                # set request.user
                setattr(request, 'user', user)  # !!

        # further checks
        if is_authenticated(user):
            set_session_key(request, '__dssoa__requesting_user', user)

            try:
                check_user_can_login(user)

            except ProfileIncompleteException:
                logger.debug('BACKEND User "{}" has incomplete profile'.format(user))

                set_session_key(request, '__dssoa__must_update_profile', True)

    # response
    def backend_process_response(self, request, response):
        # redirect to profile complete (if required)
        if get_session_key(request, '__dssoa__must_update_profile', False):
            requesting_user = get_session_key(request, '__dssoa__requesting_user')

            if self._request_path_is_disabled_for_incomplete_users(request.path):
                logger.info('Redirecting user "{}" to profile completion'.format(requesting_user))

                response = self._redirect_to_profile_complete_response(request.user)

        # invalidate JWT cookie on response (if required)
        if get_session_key(request, '__dssoa__clear_response_jwt', False):
            invalidate_cookie(response, app_settings.JWT_COOKIE_NAME)

        return response
