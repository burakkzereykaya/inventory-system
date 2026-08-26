from django.core.exceptions import ValidationError
from django.db import models
from locations.models import Location, Device
from django.conf import settings

class Ticket(models.Model):
    def clean(self):
        super().clean()
        if self.status == Ticket.TicketStatuses.In_Progress and self.assigned_to is None:
            raise ValidationError("Tickets which status are IN PROGRESS must assigned to a personnel")
        if self.pk:
           old_ticket = Ticket.objects.get(pk=self.pk)
           if old_ticket.status == Ticket.TicketStatuses.Resolved and old_ticket.status != self.status:
               raise ValidationError("The Ticket Status can not be change from Resolved to anything.")

    class Priorities(models.TextChoices):
        low ="LOW","Low",
        medium ="MED","Medium",
        high ="HIGH","High",
        critical ="CRT","Critical",
    class TicketStatuses(models.TextChoices):
        Queued="QUEUE","Queued",
        In_Progress="PROG","In Progress",
        Waiting="WAIT","Waiting",
        Deferred="DEFER","Deferred"
        Resolved="SOLVED","Resolved",


    title=models.CharField(max_length=30)
    description=models.TextField(max_length=150)
    affected_devices=models.ManyToManyField(Device,blank=True,related_name="tickets")
    affected_location=models.ForeignKey(Location,blank=True,on_delete=models.PROTECT,related_name="ticket_location",null=True)
    reported_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="reported_tickets")
    recorded_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="recorded_tickets")
    assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="assigned_tickets",null=True,blank=True)
    priority=models.CharField(choices=Priorities.choices,max_length=4)
    status=models.CharField(choices=TicketStatuses.choices,max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    resolved_at=models.DateTimeField(null=True,blank=True)

class TicketAssignmentHistory(models.Model):
        ticket =models.ForeignKey(Ticket,on_delete=models.PROTECT,related_name="ticket_assignment_history")
        previous_assignee=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="user_was_assignee",blank=True,null=True)
        new_assignee=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="user_assigned",blank=True,null=True)
        changed_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="history_changes")
        changed_at=models.DateTimeField(auto_now_add=True)
        note=models.CharField(max_length=80,blank=True)

class TicketStatusHistory(models.Model):
    ticket=models.ForeignKey(Ticket,on_delete=models.PROTECT,related_name="ticket_status_history")
    previous_status=models.CharField(choices=Ticket.TicketStatuses.choices,max_length=6,blank=True,null=True)
    new_status=models.CharField(choices=Ticket.TicketStatuses.choices,max_length=6)
    changed_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    changed_at=models.DateTimeField(auto_now_add=True)
    note=models.CharField(max_length=80,blank=True)

class TicketComment(models.Model):
    ticket=models.ForeignKey(Ticket,on_delete=models.PROTECT,related_name="comments")
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="ticket_comments")
    comment=models.TextField(max_length=360)
    created_at=models.DateTimeField(auto_now_add=True)