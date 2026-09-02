from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect

from locations.forms import DeviceForm
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
    network_interface = device.network_interfaces.all()
    status_history=(
        device.status_history
        .all()
        .order_by("-changed_at")
    )
    context={
        "device":device,
        "network_interfaces":network_interface,
        "status_history":status_history,
    }


    return render(request,"locations/device_detail.html",context)

@login_required
@permission_required('locations.add_device',raise_exception=True)
def create_device(request):
    if request.method == "POST":
        form=DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.created_by=request.user
            device.updated_by=request.user
            device.save()
            return redirect("device_detail",device_id=device.pk)

    else:
        form=DeviceForm()
    context={
            "form":form
        }
    return render(request,"locations/create_device.html",context)