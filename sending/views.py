import datetime

from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from sending import models


class HomeTemplateView(TemplateView):
    template_name = "sending/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipient"] = models.Recipient.objects.all()
        context["sendings"] = models.Sending.objects.all()

        now = datetime.datetime.now().time()
        context["active_sendings"] = models.Sending.objects.filter(start_time__lte=now, end_time__gte=now).exclude(
            start_time__isnull=True, end_time__isnull=True
        )

        return context


class RecipientListView(ListView):
    model = models.Recipient
    template_name = "sending/recipient.html"
    context_object_name = "recipient"


class RecipientCreateView(CreateView):
    model = models.Recipient
    template_name = "sending/recipient_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("sending:recipient")


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


class MessageListView(ListView):
    model = models.Messages
    template_name = "sending/message.html"
    context_object_name = "messages"


class MessageCreateView(CreateView):
    model = models.Messages
    template_name = "sending/message_form.html"
    fields = ["title", "text"]
    success_url = reverse_lazy("sending:messages")


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


class SendingListView(ListView):
    model = models.Sending
    template_name = "sending/sendings.html"
    context_object_name = "sendings"


class SendingCreateView(CreateView):
    model = models.Sending
    template_name = "sending/sendings_form.html"
    fields = ["start_time", "end_time", "message", "recipients"]
    success_url = reverse_lazy("sending:sendings")

    def form_valid(self, form):
        start = form.cleaned_data["start_time"]
        end = form.cleaned_data["end_time"]

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


def sending_mail(requests):
    now = datetime.datetime.now().time()

    if requests.method == "POST":
        sendings = models.Sending.objects.filter(start_time__lte=now, end_time__gte=now)
        if not sendings.exists():
            return redirect("sending:home")

        for sending in sendings:
            recipients_email = list(sending.recipients.all().values_list("email", flat=True))

            message_obj = models.Messages.objects.get(id=sending.message_id)
            message_text = message_obj.text

            send_mail(
                subject=message_obj.title or "Рассылка",
                message=message_text,
                from_email="noreply@example.com",
                recipient_list=recipients_email,
                fail_silently=False,
            )
        return redirect("sending:home")

    content = models.Sending.objects.filter(start_time__lt=now, end_time__gt=now)
    context = {"sendings": content}

    return render(requests, "sending/sending_mail.html", context=context)
