from django.contrib.auth import get_user_model

from django_sso_app.core.tests.factories import UserTestCase

from ...emails.models import EmailAddress
from ...groups.models import Group
from ...profiles.models import Profile

User = get_user_model()


class UserTestCase(UserTestCase):
    def test_add_profile_to_group_updates_rev(self):
        user = self._get_new_user()

        group = Group.objects.create(name='new_group')

        profile = user.sso_app_profile

        profile_rev = profile.sso_rev

        profile.groups.add(group)

        print('profile groups', profile.groups.all())

        profile.refresh_from_db()

        self.assertEqual(profile.sso_rev, profile_rev + 1)
