from django.conf import settings

from celery.task import task
from celery.utils.log import get_task_logger

from common.email.message import Email


logger = get_task_logger(__name__)


@task
def send_registration_confirmation(username: str, email: str):
    """
    Send registration confirmation email
    """
    logger.info("Sending email to: {}".format(email))
    email = Email({'username': username, 'email': email, 'app_name': settings.PROJECT_EMAIL_TEMPLATE_NAME},
                  'email/registration_confirmation.html',
                  'You was successfully registered in {}'.format(settings.PROJECT_EMAIL_TEMPLATE_NAME), [email])
    email.send()
