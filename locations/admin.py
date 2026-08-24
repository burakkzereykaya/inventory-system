from django.contrib import admin
from .models import Department, Location, DeviceType, Manufacturer, Device, NetworkInterface, IPAddress

admin.site.register(Department)
admin.site.register(Location)
admin.site.register(Manufacturer)
admin.site.register(DeviceType)
admin.site.register(NetworkInterface)
admin.site.register(IPAddress)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    readonly_fields = ("created_by","updated_by")
    def save_model(self,request,obj,form,change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request,obj,form,change)