import logging

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.utils.timezone import now

from ..utils import get_or_create_user_profile
from ..models import Profile

logger = logging.getLogger('django_sso_app.core.apps.profiles.signals')

User = get_user_model()


@receiver(pre_save, sender=Profile)
def profile_pre_updated(sender, instance, **kwargs):
    """
    Profile model has been updated, updating rev
    """
    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        return

    profile = instance

    # set profile completed_at if all required fields are set
    if not profile.is_incomplete and profile.completed_at is None:
        profile.completed_at = now()

    if not profile._state.adding:
        user = profile.user

        if getattr(user, '__dssoa__apigateway_update', False):
            logger.debug('Profile has been updted by api gateway, skipping rev update')
        elif getattr(user, '__dssoa__creating', False):
            logger.debug('Created, skipping rev update')
        else:
            logger.debug('Profile model has been updated, updating rev')
            profile.update_rev(False)


@receiver(post_save, sender=Profile)
def profile_updated(sender, instance, created, **kwargs):
    """
    Profile model has been updated, updating rev
    """
    profile = instance

    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        setattr(profile.user, '__dssoa__loaddata', True)
        return

    if not created:  # if instance.pk:
        logger.debug('Profile model has been updated, refreshing instance')
        profile.refresh_from_db()

# user

@receiver(post_save, sender=User)
def create_update_user_profile(sender, instance, created, **kwargs):
    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        # setting property flag
        setattr(instance, '__dssoa__loaddata', True)
        return

    user = instance

    if created:
        logger.debug('backend signals user created')

        setattr(instance, '__dssoa__creating', True)

        profile = get_or_create_user_profile(user, Profile, commit=True)

        logger.debug('new profile created "{}"'.format(profile))

        # refreshing user instance
        user.sso_app_profile = profile

    else:
        logger.debug('backend signals user updated')
        profile = get_or_create_user_profile(user, Profile, commit=False)
        update_rev = True

        # replaced by '__user_loggin_in'
        # if user.previous_serialized_as_string == user.serialized_as_string:
        if getattr(user, '__dssoa__creating', False):
            logger.info('user _creating')
            update_rev = False
        elif getattr(user, '__dssoa__user_loggin_in', False):
            logger.info('user loggin in')
            update_rev = False
        elif user.password_has_been_hardened:
            logger.info('password_has_been_hardened')
            update_rev = False

        if user.email_has_been_updated:
            # aligning sso_app_profile django_user_email
            profile.django_user_email = user.sso_app_new_email

        if user.username_has_been_updated:
            # aligning sso_app_profile django_user_username
            profile.django_user_username = user.sso_app_new_username

        if update_rev:
            logger.info('Update rev by User signal while user fields have been updated')
            profile.update_rev(True)  # updating rev


@receiver(user_logged_in)
def post_user_login(**kwargs):
    """
    Post login profile creation safety
    :param kwargs:
    :return:
    """
    user = kwargs['user']

    _profile = get_or_create_user_profile(user, Profile)
    # setattr(user, 'sso_app_profile', _profile)

    logger.debug('Profile, "{}" LOGGED IN!!!'.format(_profile))
