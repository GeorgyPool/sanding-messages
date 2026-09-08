from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from sending import models


def home(requests):
    return render(requests, "sending/home.html")


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
