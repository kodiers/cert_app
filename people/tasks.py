from django.conf import settings

from celery.task import task
from celery.utils.log import get_task_logger

from common.email.message import Email


logger = get_task_logger(__name__)


@task
def send_registration_confirmation(username: str, email: str) -> None:
    """
    Send registration confirmation email
    """
    logger.info("Sending registration email to: {}".format(email))
    email = Email({'username': username, 'email': email}, 'email/registration_confirmation.html',
                  'You was successfully registered in {}'.format(settings.PROJECT_EMAIL_TEMPLATE_NAME), [email])
    email.send()


@task
def send_password_reset_email(username: str, email: str, reset_url: str) -> None:
    """
    Send password reset email
    """
    logger.info("Sending password reset email to: {}".format(email))
    email = Email({'username': username, 'reset_url': reset_url}, 'email/password_reset.html', "Reset your password",
                  [email])
    email.send()
