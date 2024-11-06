from django.test import TestCase
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer

User = get_user_model()


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.valid_user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password123",
            "is_staff": False,
        }

    def test_user_serializer_with_valid_data(self):
        serializer = UserSerializer(data=self.valid_user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, self.valid_user_data["username"])
        self.assertEqual(user.email, self.valid_user_data["email"])
        self.assertEqual(user.first_name, self.valid_user_data["first_name"])
        self.assertEqual(user.last_name, self.valid_user_data["last_name"])
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password(self.valid_user_data["password"]))

    def test_user_serializer_missing_password(self):
        data_without_password = self.valid_user_data.copy()
        data_without_password.pop("password")
        serializer = UserSerializer(data=data_without_password)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_user_serializer_invalid_email(self):
        data_with_invalid_email = self.valid_user_data.copy()
        data_with_invalid_email["email"] = "not-an-email"
        serializer = UserSerializer(data=data_with_invalid_email)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_user_serializer_duplicate_username(self):
        User.objects.create_user(**self.valid_user_data)
        serializer = UserSerializer(data=self.valid_user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
