from logging import raiseExceptions

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from locations.forms import DeviceForm, NetworkInterfaceForm, IpAddressForm
from locations.models import Device, DeviceStatusHistory, NetworkInterface, IPAddress, Location, Manufacturer, \
    DeviceType


@login_required
def device_list(request):
    devices=Device.objects.all()
    device_type=request.GET.get("device_type","")
    manufacturers=Manufacturer.objects.all()
    search=request.GET.get("search","")
    status=request.GET.get("status","")
    location=request.GET.get("location","")
    manufacturer=request.GET.get("manufacturer","")
    locations=Location.objects.all()
    device_types=DeviceType.objects.all()
    if search:
        devices=devices.filter(
            Q(asset_id__icontains=search)
            |
            Q(serial_number__icontains=search)
        )
    if status:
        devices =devices.filter(status=status)
    if location:
        devices=devices.filter(location_id=location)
    if manufacturer:
        devices=devices.filter(manufacturer_id=manufacturer)
    if device_type:
        devices=devices.filter(device_type_id=device_type)

    context={
        "devices":devices,
        "search":search,
        "status":status,
        "status_choices":Device.Statuses.choices,
        "location":location,
        "locations":locations,
        "manufacturer":manufacturer,
        "manufacturers":manufacturers,
        "device_type":device_type,
        "device_types":device_types,
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


@login_required
@permission_required('locations.change_device',raise_exception=True)
def edit_device(request,device_id):
    device=get_object_or_404(Device,pk=device_id)
    previous_status=device.status
    previous_status_note=device.status_note

    if request.method == "POST":
        form=DeviceForm(request.POST,instance=device)
        if form.is_valid():
            updated_device = form.save(commit=False)
            updated_device.updated_by = request.user

            status_changed =( previous_status != updated_device.status or previous_status_note != updated_device.status_note)
            updated_device.save()


            if status_changed:
                DeviceStatusHistory.objects.create(
        device = updated_device,
        previous_status = previous_status,
        new_status = updated_device.status,
        status_note = updated_device.status_note,
        changed_by = request.user,
                )

            return redirect("device_detail", device_id=updated_device.pk)
    else:
        form =DeviceForm(instance=device)

    context = {
        "form": form,
        "device": device,
    }
    return render(request,"locations/edit_device.html",context)

@login_required
@permission_required("locations.add_networkinterface",raise_exception=True)
def add_network_interface(request,device_id):
    device=get_object_or_404(Device,pk=device_id)
    if request.method == "POST":
        form=NetworkInterfaceForm(request.POST)
        if form.is_valid():
            interface=form.save(commit=False)
            interface.device=device
            interface.save()
            return redirect("device_detail",device_id=device.id)
    else:
        form=NetworkInterfaceForm()

    context={
        "form":form,
        "device":device,
    }
    return render(request,"locations/add_network_interface.html",context)

@login_required
@permission_required("locations.add_ipaddress", raise_exception=True)
def add_ip_address(request,interface_id):
    interface=get_object_or_404(NetworkInterface,pk=interface_id)

    if request.method == "POST":
           form = IpAddressForm(request.POST)
           if form.is_valid():
                ip_address=form.save(commit=False)
                ip_address.network_interface = interface
                ip_address.save()

                return redirect("device_detail",device_id=interface.device.id)

    else:
        form=IpAddressForm()


    context={
        "form":form,
        "interface":interface,
    }

    return render(request,"locations/add_ip_address.html",context)

@login_required
@permission_required("locations.change_networkinterface",raise_exception=True)
def edit_network_interface(request,interface_id):
    interface=get_object_or_404(NetworkInterface,pk=interface_id)
    if request.method == "POST":
        form=NetworkInterfaceForm(request.POST,instance=interface)
        if form.is_valid():

            interface=form.save()

            return redirect("device_detail",device_id=interface.device.id)
    else:
        form=NetworkInterfaceForm(instance=interface)

    context={
        "form":form,
        "interface":interface,
    }

    return render(request,"locations/edit_network_interface.html",context)

@login_required
@permission_required("locations.change_ipaddress",raise_exception=True)
def edit_ip_address(request,ip_id):
    ip_address=get_object_or_404(IPAddress,pk=ip_id)
    if request.method=="POST":
        form=IpAddressForm(request.POST,instance=ip_address)
        if form.is_valid():
            updated_ip=form.save()

            return  redirect("device_detail",device_id=updated_ip.network_interface.device.id)
    else:
        form=IpAddressForm(instance=ip_address)

    context={
        "form":form,
        "ip_address":ip_address,
    }


    return render(request,"locations/edit_ip_address.html",context)