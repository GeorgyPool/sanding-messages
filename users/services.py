from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key

from .models import CustomUser


class ServiceCheckingUser:

    @staticmethod
    def get_user(user_id):

        try:
            user = CustomUser.objects.get(id=user_id)
            return user
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def activate_user(user_object):

        if not user_object:
            return None

        user_object.is_activate = True
        user_object.save()
