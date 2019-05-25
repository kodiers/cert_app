from django.core import mail
from django.test import TestCase
from django.conf import settings

from people.tasks import send_registration_confirmation, send_password_reset_email


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
