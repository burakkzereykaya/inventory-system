from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path("tickets/", views.ticket_list, name="ticket_list"),
    path("tickets/<int:ticket_id>/",views.ticket_detail,name="ticket_detail"),
    ]