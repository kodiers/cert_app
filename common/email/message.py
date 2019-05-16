from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


class Email:
    """
    Email class as wrapper to standard Django EmailMultiAlternatives class
    """
    def __init__(self, context: dict, template_name: str, subject: str, receivers: list):
        context.update({'app_name': settings.PROJECT_EMAIL_TEMPLATE_NAME})
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)
        self.message = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, receivers)
        self.message.attach_alternative(html_content, 'text/html')

    def send(self):
        """
        Send email message
        """
        self.message.send()
