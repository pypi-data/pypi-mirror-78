from django.contrib.auth import get_user_model

from django_filters import rest_framework as filters

User = get_user_model()


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['exact'],
            'sso_app_profile__sso_id': ['exact'],
            'groups__name': ['exact'],
        }
