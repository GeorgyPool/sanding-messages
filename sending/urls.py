from django.urls import path
from sending.apps import SendingConfig
from . import views

app_name = SendingConfig.name

urlpatterns = [
    path("sending/home/", views.home, name="home"),
    path("sending/recipient/", views.RecipientListView.as_view(), name="recipient"),
    path("sending/recipient_create/", views.RecipientCreateView.as_view(), name="create"),
    path("sending/recipient_detail/<int:pk>/", views.RecipientDetailView.as_view(), name="recipient_detail"),
    path("sending/recipient_update/<int:pk>/", views.RecipientUpdateView.as_view(), name="recipient_update"),
    path("sending/recipient_delete/<int:pk>/", views.RecipientDeleteView.as_view(), name="recipient_delete")
]
