import os
import datetime
import binascii
from random import seed, randint
import base64

from django.core.management.utils import get_random_secret_key
from django.conf import settings

from .exceptions import ProfileIncompleteException, DectivatedUserException, UnsubscribedUserException, DjangoStaffUsersCanNotLoginException
from .permissions import is_authenticated, is_django_staff
from . import app_settings

# initializing seed
SEED = int(base64.b16encode(bytes(get_random_secret_key(), 'utf-8')), 16)
seed(SEED)

JWT_COOKIE_SECURE = not settings.DEBUG


def set_cookie(response, key, value, days_expire=None, secure=JWT_COOKIE_SECURE):
    """
    Sets response auth cookie

    :param response:
    :param key:
    :param value:
    :param days_expire:
    :param secure:
    :return:
    """

    if days_expire is None:
        max_age = app_settings.COOKIE_AGE  # django default
    else:
        max_age = days_expire * 24 * 60 * 60

    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie(key, value, max_age=None, expires=expires, path='/',
                        domain=app_settings.COOKIE_DOMAIN,
                        secure=secure,
                        httponly=app_settings.COOKIE_HTTPONLY)

    # samesite None cookie patch
    # replaced by "same_site" middleware
    # if app_settings.SAME_SITE_COOKIE_NONE:
    #    response.cookies[key]['samesite'] = 'None'


def invalidate_cookie(response, key):
    """
    Sets response auth cookie to 'Null'

    :param response:
    :param key:
    :return:
    """
    response.set_cookie(key, '', max_age=None, expires='Thu, 01 Jan 1970 00:00:01 GMT', path='/',
                        domain=app_settings.COOKIE_DOMAIN, secure=None, httponly=False)


def set_session_key(request, key, value):
    """
    Sets django sessions request key
    :param request:
    :param key:
    :param value:
    :return:
    """

    #request.session[key] = value

    setattr(request, key, value)


def get_session_key(request, key, default=None):
    """
    Gets django sessions request key
    :param request:
    :param key:
    :param default:
    :return:
    """

    #return request.session.get(key, default)

    return getattr(request, key, default)


def check_user_can_login(user, skip_profile_checks=False):
    """
    Check user login ability
    :param user:
    :return:
    """

    if is_authenticated(user):
        if is_django_staff(user):
            raise DjangoStaffUsersCanNotLoginException()
        elif not user.is_active:
            raise DectivatedUserException()
        else:
            if user.sso_app_profile.is_unsubscribed:
                raise UnsubscribedUserException()
            else:
                if not skip_profile_checks:
                    if user.sso_app_profile.is_incomplete:
                        raise ProfileIncompleteException(app_settings.PROFILE_COMPLETE_URL)


def is_test_user(user):
    """
    Chack if user is TEST_USER
    :param user:
    :return:
    """

    return user.username == app_settings.TEST_USER_USERNAME or user.email == app_settings.TEST_USER_EMAIL


def get_random_token(length=4):
    """
    Returns random token
    :param request:
    :return:
    """
    start = randint(0, 4095 - length)
    end = start + length

    return binascii.hexlify(os.urandom(2048)).decode("utf-8")[start:end]


def get_random_fingerprint(request):
    """
    Returns random fingerprint
    :param request:
    :return:
    """
    return 'random_{}_{}'.format(id(request), get_random_token(8))
