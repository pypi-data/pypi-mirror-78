import logging

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from ....utils import set_session_key

logger = logging.getLogger('django_sso_app.core.apps.users.signals')


@receiver(user_logged_in)
def post_user_login(sender, user, request, **kwargs):

    set_session_key(request, '__dssoa__requesting_user', user)

    logger.debug('Users, "{}" LOGGED IN!!!'.format(user))
