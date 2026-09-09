from itertools import count

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from locations.models import Device
from tickets.models import Ticket

@login_required
def dashboard(request):

    total_devices=Device.objects.count()

    active_devices=Device.objects.filter(
        status=Device.Statuses.Active
    ).count()

    open_tickets = Ticket.objects.exclude(
        status=Ticket.TicketStatuses.Resolved
    ).count()

    context={
        "total_devices":total_devices,
        "active_devices":active_devices,
        "open_tickets":open_tickets,
    }

    return render(request,"core/dashboard.html",context)
