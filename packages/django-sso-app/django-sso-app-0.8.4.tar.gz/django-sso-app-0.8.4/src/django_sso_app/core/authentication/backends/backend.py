import logging

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from ...utils import set_session_key
from ...apps.profiles.models import Profile
from ...apps.api_gateway.functions import get_apigateway_sso_id

logger = logging.getLogger('django_sso_app.core.authentication.backends')
User = get_user_model()


class DjangoSsoAppApiGatewayBackendAuthenticationBackend(ModelBackend):
    """
    Authenticates by request CONSUMER_USERNAME header
    """

    backend_path = 'django_sso_app.core.authentication.backends.DjangoSsoAppApiGatewayAuthenticationBackend'

    def backend_authenticate(self, request, consumer_username, encoded_jwt, decoded_jwt):
        logger.info('BACKEND authenticating by apigateway consumer {}'.format(consumer_username))

        if consumer_username is None:
            logger.debug('consuner_username not set, skipping authentication')

            return

        try:
            sso_id = get_apigateway_sso_id(consumer_username)
            profile = Profile.objects.get(sso_id=sso_id)
            user = profile.user

        except ObjectDoesNotExist:
            logger.debug('user with apigateway consumer username "{}" does not exists'.format(consumer_username))

            return

        else:
            logger.debug('user with apigateway consumer username "{}" exists'.format(consumer_username))

            set_session_key(request, '__dssoa__requesting_user', user)

            # allauth logic
            setattr(user, 'backend', self.backend_path)

        return user


class DjangoSsoAppJwtBackendAuthenticationBackend(ModelBackend):
    """
    Authenticates by request jwt
    """

    backend_path = 'django_sso_app.core.authentication.backends.DjangoSsoAppApiGatewayAuthenticationBackend'

    def backend_authenticate(self, request, encoded_jwt, decoded_jwt):
        logger.info('BACKEND authenticating by request jwt')

        try:
            sso_id = decoded_jwt['sso_id']
            profile = Profile.objects.get(sso_id=sso_id)
            user = profile.user

        except ObjectDoesNotExist:
            logger.debug('user with sso_id "{}" does not exists'.format(sso_id))
            return

        else:
            logger.debug('user with sso_id "{}" exists'.format(sso_id))

            set_session_key(request, '__dssoa__requesting_user', user)

            # allauth logic
            setattr(user, 'backend', self.backend_path)

        set_session_key(request, '__dssoa__requesting_user', user)

        return user
