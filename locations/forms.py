from django import forms

from locations.models import Device, NetworkInterface, IPAddress


class DeviceForm(forms.ModelForm):
    class Meta:
        model=Device
        fields=["asset_id","serial_number","device_type","manufacturer","location","status","status_note","general_note"]

class NetworkInterfaceForm(forms.ModelForm):
    class Meta:
        model=NetworkInterface
        fields=["name","network_interface_type","mac_address"]
class IpAddressForm(forms.ModelForm):
    class Meta:
        model=IPAddress
        fields=["ip_address","prefix","assignment_method"]