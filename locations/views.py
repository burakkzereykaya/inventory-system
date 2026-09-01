from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404

from locations.models import Device


@login_required
def device_list(request):
    devices=Device.objects.all()

    context={
        "devices":devices
    }

    return render(request,"locations/device_list.html",context)

@login_required
def device_detail(request,device_id):

    device = get_object_or_404(Device,pk=device_id)
    context={
        "device":device
    }


    return render(request,"locations/device_detail.html",context)

