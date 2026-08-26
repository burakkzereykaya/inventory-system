from django.contrib import admin
from tickets.models import Ticket, TicketAssignmentHistory
from django.utils import timezone


class TicketAssignmentHistoryInline(admin.TabularInline):
    readonly_fields = ["previous_assignee","new_assignee","changed_by","changed_at","note"]
    model=TicketAssignmentHistory
    extra = 0
    can_delete = False
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ["recorded_by","resolved_at"]
    def save_model(self,request,obj,form,change):
        previous_assignee=None
        assignment_changed=False
        if not change:
                obj.recorded_by =request.user
                if obj.assigned_to is not None:
                    assignment_changed = True
        else:
                old_ticket = Ticket.objects.get(pk=obj.pk)
                previous_assignee=old_ticket.assigned_to
                if previous_assignee != obj.assigned_to:
                    assignment_changed=True
        if obj.status == Ticket.TicketStatuses.Resolved and obj.resolved_at is None:
                obj.resolved_at = timezone.now()

        super().save_model(request,obj,form,change)
        if assignment_changed:
            TicketAssignmentHistory.objects.create(
                ticket=obj,
                previous_assignee=previous_assignee,
                new_assignee=obj.assigned_to,
                changed_by=request.user,
            )

    inlines = [TicketAssignmentHistoryInline]