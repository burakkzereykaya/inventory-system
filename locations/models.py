from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class Department(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    department=models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="locations"
    )
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)

    def __str__(self):
        return f"{self.department.name} -{self.name}"


class DeviceType(models.Model):
    type_name=models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.type_name

class Manufacturer(models.Model):
    name=models.CharField(max_length=80,unique=True)
    is_active=models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Device(models.Model):
    statuses ={
        "AC":"Active",
        "IN":"In Storage",
        "UR":"Under Repair",
        "RE":"Retired",
        "DI":"Disposed",
    }
    asset_id=models.CharField(max_length=40,unique=True)
    serial_number=models.CharField(max_length=40)
    device_type=models.ForeignKey(DeviceType,on_delete=models.PROTECT)
    manufacturer=models.ForeignKey(Manufacturer,on_delete=models.PROTECT)
    location=models.ForeignKey(Location,on_delete=models.PROTECT)
    status=models.CharField(choices=statuses,max_length=5)
    status_note=models.CharField(max_length=100,blank=True)
    general_note=models.TextField(max_length=300,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="created_devices")
    updated_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="updated_devices")


    class Meta:
        constraints=[
            UniqueConstraint(fields=["manufacturer", "serial_number"],name="unique_manufacturer_serial"),

        ]




class NetworkInterface(models.Model):
    class NetworkInterfaceType(models.TextChoices):
        Ethernet = "ET", _("Ethernet")
        WiFi = "WF", _("Wi-Fi")
        Fiber = "FB", _("Fiber")
        Virtual = "VT", _("Virtual")
    name=models.CharField(max_length=50)
    mac_address=models.CharField(max_length=20)
    network_interface_type=models.CharField(max_length=10,choices=NetworkInterfaceType.choices)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)


    class Meta:
        constraints=[
            UniqueConstraint(fields=["device","name"],name="unique_device_name")
            ]