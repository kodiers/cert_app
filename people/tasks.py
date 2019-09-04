from django.conf import settings
from django.utils import timezone

from celery.task import task
from celery.utils.log import get_task_logger

from common.email.message import Email
from people.models import PasswordResetToken


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
def send_password_reset_email(username: str, email: str, token: str) -> None:
    """
    Send password reset email
    """
    logger.info("Sending password reset email to: {}".format(email))
    reset_url = f"{settings.FRONTEND_PASSWORD_RESET_URL}/{token}"
    email = Email({'username': username, 'reset_url': reset_url}, 'email/password_reset.html', "Reset your password",
                  [email])
    email.send()


@task
def send_password_reset_success(username: str, email: str) -> None:
    """
    Send success password reset email
    """
    logger.info(f"Sending password reset success email to {email}")
    email = Email({'username': username}, 'email/password_reset_success.html', 'Your password was successfully reset.',
                  [email])
    email.send()


@task
def clear_password_reset_tokens():
    """
    Delete expired password reset tokens.
    """
    logger.info("Delete expired password reset tokens.")
    now = timezone.now()
    PasswordResetToken.objects.filter(expire_at__lte=now).delete()
