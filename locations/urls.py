
from django.urls import path
from . import views

urlpatterns=[
    path("devices/",views.device_list,name="device_list")

]