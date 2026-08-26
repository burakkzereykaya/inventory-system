from django.contrib import admin
from .models import Department, Location, DeviceType, Manufacturer, Device, NetworkInterface, IPAddress, \
    DeviceStatusHistory

admin.site.register(Department)
admin.site.register(Location)
admin.site.register(Manufacturer)
admin.site.register(DeviceType)
admin.site.register(NetworkInterface)
admin.site.register(IPAddress)

class DeviceStatusHistoryInline(admin.TabularInline):
    readonly_fields = ["previous_status","new_status","status_note","changed_at","changed_by"]
    extra=0
    model=DeviceStatusHistory
    can_delete=False
    def has_add_permission(self,request,obj:None):
        return False

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    readonly_fields = ["created_by","updated_by"]
    list_display=[
        "asset_id",
        "serial_number",
        "device_type",
        "manufacturer",
        "location",
        "status",
        "updated_at",
    ]
    list_filter=[
        "status",
        "device_type",
        "manufacturer",
        "location",
    ]
    search_fields=[
        "asset_id",
        "serial_number",
        "status_note",
        "general_note",
    ]
    def save_model(self,request,obj,form,change):
        if not change:
            obj.created_by = request.user
        else:
            old_device = Device.objects.get(pk=obj.pk)
            previous_status = old_device.status
            old_status_note = old_device.status_note
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        if change and (previous_status != obj.status or old_status_note != obj.status_note):
            DeviceStatusHistory.objects.create(
                device=obj,
                previous_status=old_device.status,
                new_status=obj.status,
                status_note=obj.status_note,
                changed_by=request.user
            )
    inlines = [DeviceStatusHistoryInline]


