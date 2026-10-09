from django.utils import timezone

from sending.models import Recipient, Sending
from users.models import CustomUser


class AllInformation:

    @staticmethod
    def all_info_about_website() -> dict:
        """
        Возвращает общую информацию о количестве рассылок на сайте
        """
        now = timezone.now().time()

        context = {
            "recipient": Recipient.objects.all(),
            "sendings": Sending.objects.all(),
            "active_sendings": Sending.objects.filter(start_time__lte=now, end_time__gte=now).exclude(
                start_time__isnull=True, end_time__isnull=True
            ),
        }

        return context
