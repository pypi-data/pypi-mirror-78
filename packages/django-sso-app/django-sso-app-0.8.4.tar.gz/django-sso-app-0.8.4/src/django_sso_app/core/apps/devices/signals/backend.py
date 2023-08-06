import logging

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save, post_save

from allauth.account.adapter import get_adapter

from ....utils import set_session_key
from ....tokens.utils import jwt_encode
from ....functions import get_random_string
from ....permissions import is_django_staff
from ...profiles.models import Profile

from .... import app_settings

from ..models import Device
from ..utils import get_request_device

logger = logging.getLogger('django_sso_app.core.apps.devices.signals')


# profile

@receiver(post_save, sender=Profile)
def post_profile_saved(sender, instance, created, **kwargs):
    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        return

    if not created:  # if instance.pk:
        profile = instance

        logger.debug('Profile "{}" post_save signal'.format(profile))

        rev_updated = getattr(profile, '__rev_updated', False)

        if rev_updated:
            logger.info('Rev updated, removing all user devices for Profile "{}"'.format(profile))
            adapter = get_adapter()

            adapter.remove_all_user_profile_devices(profile.user)


# device

@receiver(pre_save, sender=Device)
def pre_device_save(sender, instance, **kwargs):
    if not app_settings.APIGATEWAY_ENABLED:
        user = instance.profile.user
        device = instance

        if not is_django_staff(user):
            logger.debug('Skip creating api gateway JWT for Device "{}"'.format(device))

            device.apigw_jwt_id = None
            device.apigw_jwt_key = None
            device.apigw_jwt_secret = device.apigw_jwt_secret or get_random_string(32)


@receiver(user_logged_in)
def post_user_login(**kwargs):
    user = kwargs['user']

    if not is_django_staff(user):
        request = kwargs['request']

        device = get_request_device(request)
        token = jwt_encode(device.get_jwt_payload(), device.apigw_jwt_secret)

        set_session_key(request, '__dssoa__device', device)
        set_session_key(request, '__dssoa__jwt_token', token)

        logger.info('User Logged in, request has device "{}"'.format(device))
