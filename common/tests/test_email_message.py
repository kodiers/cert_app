from unittest.mock import patch

from django.core import mail
from django.test import TestCase


from common.email.message import Email


class TestEmail(TestCase):
    """
    Test Email class
    """
    @patch('common.email.message.render_to_string', return_value='<h1>test</h1>')
    def test_email_send(self, *args, **kwargs):
        subject = 'Test subject'
        email = Email({'username': 'test'}, 'test.html', subject, ['test@test.com'])
        self.assertIsInstance(email.message, mail.EmailMultiAlternatives)
        email.send()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)