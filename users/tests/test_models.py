from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.username, "testuser")

    def test_user_str_method(self):
        self.assertEqual(str(self.user), "testuser@example.com")
