import logging

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import smart_str

from jwt.exceptions import InvalidSignatureError

from ... import app_settings
from ...utils import set_session_key, get_session_key
from ...permissions import is_authenticated, is_django_staff
from ...exceptions import RequestHasValidJwtWithNoDeviceAssociated
from ...tokens.utils import get_request_jwt, jwt_decode
from ...apps.api_gateway.functions import get_apigateway_sso_id

from .backend import DjangoSsoAppAuthenticationBackendMiddleware
from .app import DjangoSsoAppAuthenticationAppMiddleware

logger = logging.getLogger('django_sso_app.core.authentication.middleware')


ADMIN_URL = '/{}'.format(settings.ADMIN_URL)
SSO_ID_JWT_KEY = 'sso_id'
PROFILE_INCOMPLETE_ENABLED_PATHS = [
    reverse('javascript-catalog'),
    reverse('profile.complete'),
]


class DjangoSsoAppAuthenticationMiddleware(DjangoSsoAppAuthenticationBackendMiddleware,
                                           DjangoSsoAppAuthenticationAppMiddleware):
    """
    See django.contrib.auth.middleware.RemoteUserMiddleware.
    """

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "SSO middleware requires the authentication middleware to be"
                " installed.  Edit your MIDDLEWARE setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the SsoMiddleware class.")

        request_path = request.path
        request_method = request.method
        request_ip = request.META.get('REMOTE_ADDR', None)
        request_user = request.user

        logger.info('--- "{}" request "{}" path "{}" method "{}" user "{}"'.format(request_ip,
                                                                                   id(request),
                                                                                   request_path,
                                                                                   request_method,
                                                                                   request_user))

        if is_authenticated(request_user):

            if is_django_staff(request_user):
                logger.info('Skipping django staff user "{}"'.format(request_user))
                #  >= 1.10 has is_authenticated as parameter
                # If a staff user is already authenticated, we don't need to
                # continue
                set_session_key(request, '__dssoa__user', request_user)
                return

            elif request_path.startswith(ADMIN_URL):
                logger.warning('Non staff user "{}" called admin path'.format(request_user))

                self._remove_invalid_user(request)
                self._clear_response_jwt(request)

                return

            set_session_key(request, '__dssoa__requesting_user', request_user)

        # saving request info
        set_session_key(request, '__dssoa__request_ip', request_ip)

        """
        if self.request_path.startswith('/api/v1/passepartout'):
            logger.info('is passepartout path')
            # set_session_key(request, '__dssoa__is_passepartout_path', True)
        """

        try:
            request_jwt = get_request_jwt(request, encoded=False)

            if request_jwt is None:
                logger.debug('No JWT in request, skipping')

                return

            else:
                # decoding request JWT
                request_device, decoded_jwt = jwt_decode(request_jwt, verify=True)

        except KeyError:
            logger.exception('Malformed JWT "{}"'.format(request_jwt))

            self._remove_invalid_user(request)
            self._clear_response_jwt(request)

            return

        except InvalidSignatureError:
            logger.warning('Invalid JWT signature "{}"'.format(request_jwt))

            self._remove_invalid_user(request)
            self._clear_response_jwt(request)

            return

        except RequestHasValidJwtWithNoDeviceAssociated:
            logger.warning('RequestHasValidJwtWithNoDeviceAssociated "{}"'.format(request_jwt))

            self._remove_invalid_user(request)
            self._clear_response_jwt(request)

            return

        except Exception:
            logger.exception('Generic exception "{}"'.format(request_jwt))

            self._remove_invalid_user(request)
            self._clear_response_jwt(request)

            return

        apigateway_enabled = app_settings.APIGATEWAY_ENABLED
        request_jwt_sso_id = decoded_jwt[SSO_ID_JWT_KEY]

        if apigateway_enabled:
            # getting sso_id by apigateway consumer username
            try:
                consumer_username = request.META[self.header]

                if consumer_username == self.anonymous_username:
                    logger.info('consumer is anonymous, returning')

                    self._remove_invalid_user(request)

                    return

            except KeyError as e:
                # If specified header or jwt doesn't exist then remove any existing
                # authenticated user, or return (leaving request.user set to
                # AnonymousUser by the AuthenticationMiddleware).

                logger.info('Missing apigateway header "{}"'.format(e))

                self._remove_invalid_user(request)

                return

            else:
                sso_id = get_apigateway_sso_id(consumer_username)

                set_session_key(request, '__dssoa__apigateway__consumer_username', consumer_username)

        else:
            sso_id = request_jwt_sso_id

        # If the user is already authenticated and that user is active and the
        # one we are getting passed in the headers, then the correct user is
        # already persisted in the session and we don't need to continue.
        if is_authenticated(request_user):
            # double check sso_id equality between received jwt and sso_app_profile
            if smart_str(request_user.sso_id) != sso_id:

                # An authenticated user is associated with the request, but
                # it does not match the authorized user in the header.
                logger.warning('credentials and request_user sso_id differs! "{}" "{}"'.format(sso_id,
                                                                                               request_user.sso_id))

                self._remove_invalid_user(request)
                self._clear_response_jwt(request)

                return

        # authentication
        if app_settings.BACKEND_ENABLED:
            self.backend_process_request(request, request_jwt, decoded_jwt)
        else:
            self.app_process_request(request, request_jwt, decoded_jwt)

    def process_response(self, request, response):
        # getting request info
        requesting_user = get_session_key(request, '__dssoa__requesting_user')
        request_ip = get_session_key(request, '__dssoa__request_ip')

        if app_settings.BACKEND_ENABLED:
            response = self.backend_process_response(request, response)
        else:
            response = self.app_process_response(request, response)

        logger.info('--- "{}" request "{}" user "{}" path "{}" method "{}" ({})'.format(request_ip,
                                                                                        id(request),
                                                                                        requesting_user,
                                                                                        request.path,
                                                                                        request.method,
                                                                                        response.status_code))

        return response
