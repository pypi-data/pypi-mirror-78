import logging
import requests

from django.contrib.auth import get_user_model

from .... import app_settings
from .functions import get_apigateway_consumer_id

logger = logging.getLogger('django_sso_app.core.apps.api_gateway.kong')
User = get_user_model()


def get_apigw_consumer(profile):
    logger.info('getting apigw consumer for {}'.format(profile))

    consumer_id = get_apigateway_consumer_id(profile.sso_id)

    url = app_settings.APIGATEWAY_HOST + "/consumers/{}".format(consumer_id)
    r = requests.get(url)

    response_body = None
    status_code = r.status_code
    try:
        response_body = r.json()
    except:
        logger.info('Response ({}) has no payload'.format(status_code))

    logger.info('apigw response ({0}) {1}'.format(status_code, response_body))
    return status_code, response_body


def create_apigw_consumer(profile):
    logger.info('creating apigw consumer for {}'.format(profile))

    consumer_id = get_apigateway_consumer_id(profile.sso_id)

    url = app_settings.APIGATEWAY_HOST + "/consumers/"
    data = {'username': consumer_id}

    r = requests.post(url, json=data)

    response_body = None
    status_code = r.status_code
    try:
        response_body = r.json()
    except:
        logger.info('Response ({}) has no payload'.format(status_code))

    logger.info('apigw response ({0}) {1}'.format(status_code, response_body))
    return status_code, response_body


def delete_apigw_consumer(profile):
    consumer_id = get_apigateway_consumer_id(profile.sso_id)
    logger.info('deleting apigw consumer for {}'.format(profile))

    url = app_settings.APIGATEWAY_HOST + "/consumers/" + consumer_id

    r = requests.delete(url)

    response_body = None
    status_code = r.status_code
    try:
        response_body = r.json()
    except:
        logger.info('Response ({}) has no payload'.format(status_code))

    logger.info('apigw response ({0}) {1}'.format(status_code, response_body))
    return status_code, response_body


def create_apigw_consumer_jwt(profile):
    consumer_id = get_apigateway_consumer_id(profile.sso_id)
    logger.info('creating apigw consumer jwt for {}'.format(profile))

    url = app_settings.APIGATEWAY_HOST + "/consumers/" + consumer_id + "/jwt/"
    data = {}

    r = requests.post(url, json=data)

    response_body = None
    status_code = r.status_code
    try:
        response_body = r.json()
    except:
        logger.info('Response ({}) has no payload'.format(status_code))

    logger.info('apigw response ({0}) {1}'.format(status_code, response_body))
    return status_code, response_body


def delete_apigw_consumer_jwt(profile, jwt_id):
    consumer_id = get_apigateway_consumer_id(profile.sso_id)
    logger.info('deleting apigw consumer jwt for {}'.format(profile))

    url = '{}/{}/{}/jwt/{}'.format(app_settings.APIGATEWAY_HOST, "consumers", consumer_id, jwt_id)

    logger.info('calling kong url "{}"'.format(url))

    r = requests.delete(url)

    status_code = r.status_code

    logger.info('apigw response ({0}) {1}'.format(status_code, None))
    return r.status_code, None


def get_apigw_consumer_jwts(profile):
    consumer_id = get_apigateway_consumer_id(profile.sso_id)
    logger.info('getting apigw consumer jwts for {}'.format(profile))

    url = app_settings.APIGATEWAY_HOST + "/consumers/" + consumer_id + "/jwt/"

    r = requests.get(url)

    response_body = None
    status_code = r.status_code
    try:
        response_body = r.json()
    except:
        logger.info('Response ({}) has no payload'.format(status_code))

    logger.info('apigw response ({0}) {1}'.format(status_code, response_body))
    return status_code, response_body


def create_apigw_consumer_acl(profile, group_name=app_settings.APIGATEWAY_CONSUMER_GROUP):
    consumer_id = get_apigateway_consumer_id(profile.sso_id)
    logger.info('creating apigw consumer acl {} for {}'.format(group_name,
                                                               profile))

    url = app_settings.APIGATEWAY_HOST + "/consumers/" + consumer_id + "/acls/"
    data = {"group": group_name}

    r = requests.post(url, json=data)

    response_body = None
    status_code = r.status_code
    try:
        response_body = r.json()
    except:
        logger.info('Response ({}) has no payload'.format(status_code))

    logger.info('apigw response ({0}) {1}'.format(status_code, response_body))
    return status_code, response_body


def get_apigw_consumer_acls(profile):
    consumer_id = get_apigateway_consumer_id(profile.sso_id)
    logger.info('getting apigw consumer groups for {}'.format(profile))

    url = app_settings.APIGATEWAY_HOST + "/consumers/" + consumer_id + "/acls/"

    r = requests.get(url)

    response_body = None
    status_code = r.status_code
    try:
        response_body = r.json()
    except:
        logger.info('Response ({}) has no payload'.format(status_code))

    logger.info('apigw response ({0}) {1}'.format(status_code, response_body))
    return status_code, response_body


def delete_apigw_consumer_acl(profile, group_name):
    consumer_id = get_apigateway_consumer_id(profile.sso_id)
    logger.info('deleting apigw consumer acl {} for {}'.format(group_name,
                                                               profile))

    url = app_settings.APIGATEWAY_HOST + "/consumers/" + consumer_id + "/acls/" + group_name

    r = requests.delete(url)

    status_code = r.status_code

    logger.info('apigw response ({0}) {1}'.format(status_code, None))
    return r.status_code, None


def get_profile_apigw_consumer_id(profile, force_recreate=False):

    if profile.apigw_consumer_id is None or force_recreate:
        logger.info('Profile "{}" has no apigateway_consumer_id, checking if exists or creating new'.format(profile))

        # try to find an existent consumer
        status_code_0, consumer = get_apigw_consumer(profile)
        if status_code_0 == 404:
            logger.info('No apigw consumer found for profile "{}", creating'.format(profile))

            # creating new
            status_code_1, consumer = create_apigw_consumer(profile)
            if status_code_1 != 201:
                logger.error('Error ({0}) creating apigw consumer, {1}'.format(
                    status_code_1, consumer))
                raise Exception(
                    "Error ({0}) creating apigw consumer, {1}".format(
                        status_code_1, consumer))

        elif status_code_0 == 200:
            logger.info('Consumer "{}" found for profile "{}"'.format(consumer, profile))
        else:
            raise Exception(
                "Error ({0}) getting apigw consumer, {1}".format(status_code_0, consumer))

        # adding profile to groups
        profile_groups = [app_settings.APIGATEWAY_CONSUMER_GROUP] + \
                         list(profile.user.groups.values_list('name', flat=True))

        for group_name in profile_groups:
            status_code_2, acl = create_apigw_consumer_acl(profile, group_name)
            if status_code_2 != 201:
                # delete_apigw_consumer(username)
                logger.error(
                    'Error ({0}) creating apigw consumer acl, {1}'.format(
                        status_code_2, acl))
                raise Exception(
                    "Error {0} creating apigw consumer acl, {1}".format(
                        status_code_2, acl))

        # Inhibite sso_rev update
        setattr(profile.user, '__dssoa__apigateway_update', True)
        # saving profile
        profile.apigw_consumer_id = consumer['id']
        profile.save()

    else:
        logger.info('Profile {} already has apigateway_consumer_id'.format(profile))

    return profile.apigw_consumer_id
