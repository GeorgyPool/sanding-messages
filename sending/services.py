from datetime import datetime

from sending.models import Messages, Recipient, Sending


class AllInformation:

    @staticmethod
    def all_info_about_website() -> dict:
        """
        Возвращает общую информацию о количестве рассылок на сайте
        """
        now = datetime.now().time()

        context = {
            "recipient": Recipient.objects.all(),
            "sendings": Sending.objects.all(),
            "active_sendings": Sending.objects.filter(start_time__lte=now, end_time__gte=now).exclude(
                start_time__isnull=True, end_time__isnull=True
            ),
        }

        return context


class AllInfoForUser:
    """
    Возвращает пользователю информацию о его:
    рассылках
    сообщениях
    получателях
    """

    @staticmethod
    def get_all_recipient_for_his_user(user_id: int):
        recipient = Recipient.objects.filter(owner_id=user_id)
        return recipient

    @staticmethod
    def get_all_messages_for_his_user(user_id: int):
        messages = Messages.objects.filter(owner_id=user_id)
        return messages

    @staticmethod
    def get_all_sending_for_his_user(user_id: int):
        sending = Sending.objects.filter(owner_id=user_id)
        return sending
