from django.core import mail
from django.test import TestCase
from django.conf import settings

from people.tasks import send_registration_confirmation


class TestSendRegistrationConfirmation(TestCase):
    """
    Test send_registration_confirmation
    """
    def setUp(self) -> None:
        self.username = 'test'
        self.email = 'test'

    def test_send_registration_confirmation(self):
        send_registration_confirmation(self.username, self.email)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'You was successfully registered in {}'.format(
            settings.PROJECT_EMAIL_TEMPLATE_NAME))
