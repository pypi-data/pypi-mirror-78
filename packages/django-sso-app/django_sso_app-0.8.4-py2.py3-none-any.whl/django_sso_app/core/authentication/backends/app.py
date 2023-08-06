import logging

from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlencode
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from ...apps.users.utils import fetch_remote_user, create_local_user_from_remote_backend, \
                              update_local_user_from_remote_backend, create_local_user_from_jwt, \
                              create_local_user_from_apigateway_headers

from ...apps.profiles.models import Profile
from ...apps.groups.utils import update_profile_groups
from ...exceptions import ServiceSubscriptionRequiredException, ProfileIncompleteException
from ...apps.api_gateway.functions import get_apigateway_sso_id, get_apigateway_profile_groups_from_header
from ...utils import set_session_key
from ... import app_settings


logger = logging.getLogger('django_sso_app.core.authentication.backends')
User = get_user_model()


class DjangoSsoAppAppBaseAuthenticationBackend(ModelBackend):

    def try_replicate_user(self, request, sso_id, encoded_jwt, decoded_jwt):
        logger.debug('try_replicate_user')

        if app_settings.REPLICATE_PROFILE:
            logger.info('Replicate user with sso_id "{}" from remote backend'.format(sso_id))

            # create local profile from SSO
            backend_user = fetch_remote_user(sso_id=sso_id, encoded_jwt=encoded_jwt)
            backend_user_profile = backend_user['profile']

            if backend_user_profile.get('is_incomplete', False):
                self.redirect_to_profile_complete(request.user)

            user = create_local_user_from_remote_backend(backend_user)

        else:
            user = None

        return user

    def try_update_user(self, sso_id, user, user_profile, encoded_jwt, decoded_jwt):
        logger.debug('try_update_user')

        rev_changed = user_profile.sso_rev < decoded_jwt['sso_rev']
        first_access = not user.is_active and not user_profile.is_unsubscribed

        if rev_changed or first_access:
            if rev_changed:
                logger.info('Rev changed from "{}" to "{}" for user "{}", updating ...'
                            .format(user_profile.sso_rev, decoded_jwt['sso_rev'],
                                    user))
            if first_access:
                logger.info('"{} first access, updating ...'.format(user))

            # update local profile from SSO
            setattr(user, '__dssoa__apigateway_update', True)

            remote_user = fetch_remote_user(sso_id=sso_id, encoded_jwt=encoded_jwt)
            user = update_local_user_from_remote_backend(remote_user=remote_user,
                                                         profile=user_profile)

            logger.info('{} updated with latest data from SSO'.format(user))

        else:
            logger.info('Nothing changed for apigateway consumer "{}"'.format(user))

        return user

    def try_update_profile_subscriptions(self, user):
        # Redirect user to Term Of Service.
        # is_to_subscribe = getattr(user, '__dssoa__is_to_subscribe', False)
        if user and app_settings.SERVICE_SUBSCRIPTION_REQUIRED:
            logger.debug('update subscriptions check for "{}":"{}"'.format(app_settings.SERVICE_URL,
                                                                           app_settings.SERVICE_SUBSCRIPTION_REQUIRED))

            if app_settings.REPLICATE_PROFILE:
                logger.debug('Check app subscription')

                remote_user = getattr(user, '__dssoa__remote_user', None)

                if remote_user is not None:
                    remote_profile_subscriptions = remote_user['profile']['subscriptions']
                    logger.debug('remote_profile_subscriptions "{}"'.format(remote_profile_subscriptions))

                    active_subscriptions = []
                    for s in remote_profile_subscriptions:
                        if not s['is_unsubscribed']:
                            active_subscriptions.append(s['service_url'])

                    if app_settings.SERVICE_URL not in active_subscriptions:
                        self.redirect_to_service_subscription(user)

    def redirect_to_service_subscription(self, user):
        _qs = urlencode({'next': app_settings.SERVICE_URL})
        _url = '{}{}?{}'.format(app_settings.BACKEND_URL, app_settings.LOGIN_URL, _qs)

        logger.info('User {} must agree to the Terms of Service,'
                    ' redirecting to {} ...'
                    .format(user, _url))

        response = HttpResponseRedirect(redirect_to=_url)

        raise ServiceSubscriptionRequiredException(response)

    def redirect_to_profile_complete(self, user):
        _qs = urlencode({'next': app_settings.SERVICE_URL})
        _url = '{}{}?{}'.format(app_settings.BACKEND_URL, app_settings.PROFILE_COMPLETE_URL, _qs)

        logger.info('User {} must complete profile,'
                    ' redirecting to {} ...'
                    .format(user, _url))

        response = HttpResponseRedirect(redirect_to=_url)

        raise ProfileIncompleteException(response)


class DjangoSsoAppApiGatewayAppAuthenticationBackend(DjangoSsoAppAppBaseAuthenticationBackend):
    """
    Authenticates by request CONSUMER_USERNAME header
    """

    def try_replicate_user(self, request, sso_id, encoded_jwt, decoded_jwt):
        user = super(DjangoSsoAppApiGatewayAppAuthenticationBackend, self).try_replicate_user(request, sso_id, encoded_jwt, decoded_jwt)

        if user is None:
            logger.info('Creating user from headers')

            user = create_local_user_from_apigateway_headers(request)

        return user

    def try_update_profile_groups(self, request, user):
        if app_settings.MANAGE_USER_GROUPS:
            logger.info('Updating profile groups for "{}"'.format(user))

            consumer_groups_header = request.META.get(app_settings.APIGATEWAY_CONSUMER_GROUPS_HEADER, None)
            profile_groups = get_apigateway_profile_groups_from_header(consumer_groups_header)

            update_profile_groups(user.sso_app_profile, profile_groups)

    def app_authenticate(self, request, consumer_username, encoded_jwt, decoded_jwt):
        logger.info('APP authenticating by apigateway consumer {}'.format(consumer_username))

        try:
            sso_id = get_apigateway_sso_id(consumer_username)
            profile = Profile.objects.get(sso_id=sso_id)
            user = profile.user

        except ObjectDoesNotExist:
            logger.info('No profile with id "{}"'.format(sso_id))
            try:
                user = self.try_replicate_user(request, sso_id, encoded_jwt, decoded_jwt)

            except ProfileIncompleteException:
                raise

            except Exception:
                logger.exception('Can not replicate user')

                return

        else:
            if app_settings.REPLICATE_PROFILE:
                logger.debug('Must update profile')

                if decoded_jwt is None:
                    logger.warning('decoded_jwt not set')
                    return

                user = self.try_update_user(sso_id, user, profile, encoded_jwt, decoded_jwt)

        # update user profile relations
        self.try_update_profile_groups(request, user)
        self.try_update_profile_subscriptions(user)

        return user


class DjangoSsoAppJwtAppAuthenticationBackend(DjangoSsoAppAppBaseAuthenticationBackend):
    """
    Authenticates by request jwt
    """

    def try_replicate_user(self, request, sso_id, encoded_jwt, decoded_jwt):

        user = super(DjangoSsoAppJwtAppAuthenticationBackend, self).try_replicate_user(request, sso_id, encoded_jwt, decoded_jwt)

        if user is None:
            # create local profile from jwt
            logger.info('Replicating user with sso_id "{}" from JWT'.format(sso_id))

            user = create_local_user_from_jwt(decoded_jwt)

        return user

    def try_update_profile_groups(self, request, user):
        # Update user groups
        if app_settings.MANAGE_USER_GROUPS:
            if app_settings.REPLICATE_PROFILE:
                logger.info('try_update_profile_groups for "{}"'.format(user))

                remote_user_object = getattr(user, '__dssoa__remote_user', None)

                if remote_user_object is not None:
                    remote_user_object_groups = remote_user_object.get('groups', [])

                    update_profile_groups(user.sso_app_profile, remote_user_object_groups)

    def app_authenticate(self, request, encoded_jwt, decoded_jwt):
        logger.info('backend authenticating by request jwt')

        if encoded_jwt is None or decoded_jwt is None:
            logger.debug('request jwt not set, skipping authentication')

            return

        try:
            sso_id = decoded_jwt['sso_id']
            user_profile = Profile.objects.get(sso_id=sso_id)
            user = user_profile.user

            if app_settings.REPLICATE_PROFILE:
                logger.debug('try_update_user "{}" jwt consumer "{}"'.format(sso_id, sso_id))

                user = self.try_update_user(sso_id, user, user_profile, encoded_jwt, decoded_jwt)

            else:
                # just updates user groups
                logger.debug('Do not replicate profile')

        except ObjectDoesNotExist:
            try:
                user = self.try_replicate_user(request, sso_id, encoded_jwt, decoded_jwt)

            except ProfileIncompleteException:
                raise

            except Exception:
                logger.exception('cannot replicate remote user')
                return

        # update relations
        self.try_update_profile_groups(request, user)
        self.try_update_profile_subscriptions(user)

        set_session_key(request, '__dssoa__requesting_user', user)

        return user
