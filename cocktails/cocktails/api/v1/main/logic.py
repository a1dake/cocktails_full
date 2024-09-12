import logging
import random
import string
from rest_framework.authtoken.models import Token
from apps.user.models import *

logger = logging.getLogger(__name__)

POSSIBLE_ATTEMPTS = 2


def create_auth_token(user: User) -> str:
    token = Token.objects.filter(user=user).only('key').first()  # noqa
    if token:
        return token.key

    token = Token.objects.create(user=user)
    return token.key


def get_code(length):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return code