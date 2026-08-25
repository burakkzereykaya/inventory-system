from django.contrib import admin
from django.core.exceptions import ValidationError
from tickets.models import Ticket
from django.utils import timezone

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ["recorded_by","resolved_at"]
    def save_model(self,request,obj,form,change):
        if not change:
            obj.recorded_by =request.user
        if obj.status == Ticket.TicketStatuses.Resolved and obj.resolved_at is None:
            obj.resolved_at = timezone.now()
        old_ticket=Ticket.objects.get(pk=obj.pk)


        super().save_model(request,obj,form,change)