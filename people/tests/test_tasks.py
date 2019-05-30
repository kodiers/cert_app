from datetime import timedelta

from django.core import mail
from django.test import TestCase
from django.conf import settings
from django.utils import timezone

from people.models import PasswordResetToken
from people.tasks import (
    send_registration_confirmation,
    send_password_reset_email,
    send_password_reset_success,
    clear_password_reset_tokens
)
from people.tests.recipes import user_recipe


class TestSendRegistrationConfirmation(TestCase):
    """
    Test send_registration_confirmation
    """
    def test_send_registration_confirmation(self):
        send_registration_confirmation('test', 'test@test.com')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'You was successfully registered in {}'.format(
            settings.PROJECT_EMAIL_TEMPLATE_NAME))


class TestSendPasswordResetEmail(TestCase):
    """
    Test send_password_reset_email
    """
    def test_send_password_reset_email(self):
        send_password_reset_email('test', 'test@test.com', 'sometesttoken')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Reset your password")


class TestSendPasswordResetSuccess(TestCase):
    """
    Test send_password_reset_success
    """
    def test_send_password_reset_success(self):
        send_password_reset_success('test', 'test@test.com')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Your password was successfully reset.')


class TestClearPasswordResetTokens(TestCase):
    """
    Test clear_password_reset_tokens
    """
    def test_clear_password_reset_tokens(self):
        user = user_recipe.make()
        token = PasswordResetToken.create_password_reset_token(user.email)
        self.assertEqual(PasswordResetToken.objects.count(), 1)
        token.expire_at = timezone.now() - timedelta(days=1)
        token.save()
        clear_password_reset_tokens()
        self.assertFalse(PasswordResetToken.objects.exists())
