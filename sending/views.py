import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from config.settings import EMAIL_HOST_USER
from sending import models
from sending.services import AllInfoForUser, AllInformation


class HomeTemplateView(TemplateView):
    template_name = "sending/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = AllInformation.all_info_about_website()

        return context


class RecipientListView(LoginRequiredMixin, ListView):
    model = models.Recipient
    template_name = "sending/recipient.html"
    context_object_name = "recipient"

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.user.id
        queryset = AllInfoForUser.get_all_recipient_for_his_user(user_id=user_id)

        return queryset


class RecipientCreateView(CreateView):
    model = models.Recipient
    template_name = "sending/recipient_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("sending:recipient")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientDetailView(DetailView):
    model = models.Recipient
    template_name = "sending/recipient_detail.html"
    context_object_name = "recipient"


class RecipientUpdateView(UpdateView):
    model = models.Recipient
    template_name = "sending/recipient_form.html"
    fields = ["email", "full_name", "comment"]

    def get_success_url(self):
        return reverse_lazy("sending:recipient_detail", kwargs={"pk": self.object.pk})


class RecipientDeleteView(DeleteView):
    model = models.Recipient
    template_name = "sending/recipient_delete.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("sending:recipient")


class MessageListView(LoginRequiredMixin, ListView):
    model = models.Messages
    template_name = "sending/message.html"
    context_object_name = "messages"

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.user.id
        queryset = AllInfoForUser.get_all_messages_for_his_user(user_id=user_id)

        return queryset


class MessageCreateView(CreateView):
    model = models.Messages
    template_name = "sending/message_form.html"
    fields = ["title", "text"]
    success_url = reverse_lazy("sending:messages")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageDetailView(DetailView):
    model = models.Messages
    template_name = "sending/message_detail.html"
    context_object_name = "messages"


class MessageUpdateView(UpdateView):
    model = models.Messages
    fields = ["title", "text"]
    template_name = "sending/message_form.html"

    def get_success_url(self):
        return reverse_lazy("sending:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(DeleteView):
    model = models.Messages
    template_name = "sending/message_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("sending:messages")


class SendingListView(LoginRequiredMixin, ListView):
    model = models.Sending
    template_name = "sending/sendings.html"
    context_object_name = "sendings"

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.user.id
        queryset = AllInfoForUser.get_all_sending_for_his_user(user_id=user_id)

        return queryset


class SendingCreateView(CreateView):
    model = models.Sending
    template_name = "sending/sendings_form.html"
    fields = ["start_time", "end_time", "message", "recipients"]
    success_url = reverse_lazy("sending:sendings")

    def form_valid(self, form):
        start = form.cleaned_data["start_time"]
        end = form.cleaned_data["end_time"]
        form.instance.owner = self.request.user

        if start >= end:
            form.add_error("end_time", "Время окончания должно быть позже времени начала.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class SendingDetailView(DetailView):
    model = models.Sending
    template_name = "sending/sendings_detail.html"
    context_object_name = "sendings"

    def get_object(self, queryset=None):
        result = super().get_object(queryset)

        if result.start_time > datetime.datetime.now().time():
            result.status = models.Sending.CREATE
            result.save()
            return result
        elif result.end_time < datetime.datetime.now().time():
            result.status = models.Sending.END
            result.save()
            return result
        else:
            result.status = models.Sending.LAUNCHED
            result.save()
            return result


class SendingUpdateView(UpdateView):
    model = models.Sending
    template_name = "sending/sendings_form.html"
    fields = ["start_time", "end_time", "message", "recipients"]

    def get_success_url(self):
        return reverse_lazy("sending:sendings_detail", kwargs={"pk": self.object.pk})


class SendingDeleteView(DeleteView):
    model = models.Sending
    template_name = "sending/sendings_delete.html"
    context_object_name = "sendings"
    success_url = reverse_lazy("sending:sendings")


def sending_mail(requests, pk):
    now = datetime.datetime.now().time()
    sending_user = models.Sending.objects.filter(owner_id=pk, start_time__lte=now, end_time__gte=now)

    if requests.method == "POST":
        if not sending_user.exists():
            redirect("sending:home")

        for send in sending_user:
            recipient_list = list(send.recipients.all().values_list("email", flat=True))
            recipient_message = models.Messages.objects.get(id=send.message_id)

            try:
                send_mail(
                    subject=recipient_message.title,
                    message=recipient_message.text,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=recipient_list,
                )

                models.TryingSending.objects.create(
                    status=models.TryingSending.SUCCESS, server_response="OK", mailing=send, owner=send.owner
                )

                return redirect("sending:home")

            except Exception as e:

                models.TryingSending.objects.create(
                    status=models.TryingSending.NOT_SUCCESS,
                    server_response=f"Возникла ошибка {type(e)}",
                    mailing=send,
                )

    context = {"sendings": sending_user}
    return render(requests, "sending/sending_mail.html", context=context)
