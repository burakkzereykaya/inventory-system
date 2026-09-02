from django import forms

from locations.models import Device


class DeviceForm(forms.ModelForm):
    class Meta:
        model=Device
        fields=["asset_id","serial_number","device_type","manufacturer","location","status","status_note","general_note"]