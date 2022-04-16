from django.urls import path
from . import views as form_views

urlpatterns = [
    path('email/', form_views.write_email),
    path('send_email/', form_views.send_email),
]