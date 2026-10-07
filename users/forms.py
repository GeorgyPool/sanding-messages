from django.contrib.auth.forms import UserCreationForm, forms

from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"class": "form-control"})

        self.fields["password1"].widget.attrs.update({"class": "form-control"})

        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class ChangeProfileUser(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = (
            "password",
            "is_active",
            "is_staff",
            "date_joined",
            "groups",
            "is_superuser",
            "user_permissions",
            "last_login",
        )

    def __init__(self, *args, **kwargs):
        super(ChangeProfileUser, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Введите Ник"})

        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Ваше имя"})

        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Ваша фамилия"})

        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Электронная почта"})

        self.fields["phone_number"].widget.attrs.update({"class": "form-control", "placeholder": "Телефон"})
