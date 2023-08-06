import pytest

from django_sso_app.backend.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_rest_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"
