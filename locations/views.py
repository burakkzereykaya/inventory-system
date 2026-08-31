from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from locations.models import Device


@login_required
def device_list(request):
    devices=Device.objects.all()

    context={
        "devices":devices
    }

    return render(request,"locations/device_list.html",context)

