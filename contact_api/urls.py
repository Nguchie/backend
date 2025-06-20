from django.urls import path
from . import views

urlpatterns = [
    path('send-email/', views.send_contact_email, name='send_contact_email'),
    path('schedule-call/', views.schedule_call, name='schedule_call'),
]