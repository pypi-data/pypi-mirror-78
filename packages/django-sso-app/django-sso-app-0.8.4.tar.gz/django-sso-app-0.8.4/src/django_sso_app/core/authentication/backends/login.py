import logging

from allauth.account.auth_backends import AuthenticationBackend as allauth_AuthenticationBackend

from ...permissions import is_authenticated
from ...utils import set_session_key

logger = logging.getLogger('django_sso_app.core.authentication.backends')


class DjangoSsoAppLoginAuthenticationBackend(allauth_AuthenticationBackend):
    def authenticate(self, request, **credentials):
        user = super(DjangoSsoAppLoginAuthenticationBackend, self).authenticate(request, **credentials)

        if is_authenticated(user):
            logger.debug('"{}" is authenticated'.format(user))

            set_session_key(request, '__dssoa__requesting_user', user)

            return user
