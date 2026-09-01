
from django.urls import path
from . import views

urlpatterns=[
    path("devices/",views.device_list,name="device_list"),
    path("devices/<int:device_id>/",views.device_detail,name="device_detail"),
]