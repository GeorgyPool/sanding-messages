from django.shortcuts import render
from sending import models
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy


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
