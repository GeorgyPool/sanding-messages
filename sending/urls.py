from django.urls import path

from sending.apps import SendingConfig

from . import views

app_name = SendingConfig.name

urlpatterns = [
    path("sending/home/", views.HomeTemplateView.as_view(), name="home"),
    path("sending/recipient/", views.RecipientListView.as_view(), name="recipient"),
    path("sending/recipient_create/", views.RecipientCreateView.as_view(), name="recipient_create"),
    path("sending/recipient_detail/<int:pk>/", views.RecipientDetailView.as_view(), name="recipient_detail"),
    path("sending/recipient_update/<int:pk>/", views.RecipientUpdateView.as_view(), name="recipient_update"),
    path("sending/recipient_delete/<int:pk>/", views.RecipientDeleteView.as_view(), name="recipient_delete"),
    path("sending/messages/", views.MessageListView.as_view(), name="messages"),
    path("sending/message_create/", views.MessageCreateView.as_view(), name="message_create"),
    path("sending/message_detail/<int:pk>/", views.MessageDetailView.as_view(), name="message_detail"),
    path("sending/message_update/<int:pk>/", views.MessageUpdateView.as_view(), name="message_update"),
    path("sending/message_delete/<int:pk>/", views.MessageDeleteView.as_view(), name="message_delete"),
    path("sending/sendings/", views.SendingListView.as_view(), name="sendings"),
    path("sending/sendings_create/", views.SendingCreateView.as_view(), name="sendings_create"),
    path("sending/sendings_detail/<int:pk>/", views.SendingDetailView.as_view(), name="sendings_detail"),
    path("sending/sendings_update/<int:pk>/", views.SendingUpdateView.as_view(), name="sendings_update"),
    path("sending/sendings_delete/<int:pk>/", views.SendingDeleteView.as_view(), name="sendings_delete"),
    path("sending/sendings_send/", views.sending_mail, name="sendings_send"),
]
