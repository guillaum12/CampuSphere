from django.urls import path

from .views import connexion, registration

urlpatterns = [
    path("connexion/", connexion, name="connexion"),
    path("registration/", registration, name="registration"),
]
