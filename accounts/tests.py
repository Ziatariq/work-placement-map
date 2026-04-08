from django.test import TestCase
from django.urls import reverse

from accounts.models import AllowedSignupEmail, User


class AuthFlowTests(TestCase):
    def test_restricted_signup_creates_user_and_marks_allowlist_registered(self):
        allowed = AllowedSignupEmail.objects.create(email="approved@example.com", role=User.Roles.COORDINATOR)

        response = self.client.post(
            reverse("accounts:sign_up"),
            {
                "email": "approved@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("core:home"))
        user = User.objects.get(email="approved@example.com")
        allowed.refresh_from_db()
        self.assertEqual(user.role, User.Roles.COORDINATOR)
        self.assertTrue(allowed.is_registered)

    def test_signup_rejects_unapproved_email(self):
        response = self.client.post(
            reverse("accounts:sign_up"),
            {
                "email": "blocked@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This email is not allowed to sign up")

    def test_login_invalid_shows_expected_message(self):
        User.objects.create_user(email="viewer@example.com", password="CorrectPass123!", role=User.Roles.VIEWER)

        response = self.client.post(
            reverse("accounts:login"),
            {
                "email": "viewer@example.com",
                "password": "WrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid login credentials")

    def test_login_success_redirects_home(self):
        User.objects.create_user(email="viewer@example.com", password="CorrectPass123!", role=User.Roles.VIEWER)

        response = self.client.post(
            reverse("accounts:login"),
            {
                "email": "viewer@example.com",
                "password": "CorrectPass123!",
            },
        )

        self.assertRedirects(response, reverse("core:home"))
