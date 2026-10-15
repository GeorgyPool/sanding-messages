from django.contrib.auth.forms import forms
from django.core.exceptions import ValidationError

from sending.models import Sending
from sending.services import AllInfoForUser


class FormSendingCreateView(forms.ModelForm):
    class Meta:
        model = Sending
        exclude = ("status", "owner")

    def __init__(self, *args, **kwargs):
        super(FormSendingCreateView, self).__init__(*args, **kwargs)

        self.fields["start_time"].widget.attrs.update({"class": "form-control"})

        self.fields["end_time"].widget.attrs.update({"class": "form-control"})

        self.fields["message"].widget.attrs.update({"class": "form-control"})

        self.fields["recipients"].widget.attrs.update({"class": "form-control"})

    def clean(self):
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")

        if start_time > end_time:
            raise ValidationError("Время старта не может быть больше чем конечное время")

        return self.cleaned_data
