from .test_setup import TestSetup

from apps.authentication.models import User

# import pdb
# pdb.set_trace()


class TestViews(TestSetup):
    def test_user_cannot_register(self):
        """Ensures a user cannot register with no data"""
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_can_register(self):
        """Ensures a user can register with username, email and password"""
        res = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(res.data.get("email"), self.user_data.get("email"))
        self.assertEqual(res.data.get("username"), self.user_data.get("username"))
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_login(self):
        """Ensures a user cannot login with unverified email"""
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 401)

    def test_user_can_login(self):
        """Ensures a user can login after verification"""
        register_response = self.client.post(
            self.register_url, self.user_data, format="json"
        )
        email = register_response.data.get("email")
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        login_response = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(login_response.status_code, 200)
