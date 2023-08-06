from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

# this return left time
from drf_expiring_token.models import ExpiringToken
from drf_expiring_token.settings import custom_settings


# token checker if token expired or not
def is_token_expired(token):
    return token.expires - timezone.now() < timedelta(seconds=0)


# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = ExpiringToken.objects.create(user=token.user)
    return is_expired, token


# ________________________________________________
# DEFAULT_AUTHENTICATION_CLASSES
class ExpiringTokenAuthentication(TokenAuthentication):
    """
    If token is expired then it will be removed
    and new one with different key will be created
    """

    @transaction.atomic()
    def authenticate_credentials(self, key):
        try:
            token = ExpiringToken.objects.select_related('user').get(key=key)
        except ExpiringToken.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")

        if not token.user.is_active:
            raise AuthenticationFailed("User is not active")

        is_expired, token = token_expire_handler(token)
        if is_expired:
            raise AuthenticationFailed("The Token is expired")

        token.expires = timezone.now() + custom_settings.EXPIRING_TOKEN_DURATION
        token.save()

        return token.user, token
