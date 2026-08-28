from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import  login_required
from .models import Ticket
from .forms import TicketForm

@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()

    context={
        "tickets":tickets
    }



    return render(request,"tickets/ticket_list.html",context)

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket,pk=ticket_id)
    context={
        "ticket":ticket
    }

    return render(request,"tickets/ticket_detail.html",context)

@login_required()
def create_ticket(request):
    if request.method == "POST":
        form=TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.reported_by=request.user
            ticket.recorded_by=request.user
            ticket.status=Ticket.TicketStatuses.Queued
            ticket.assigned_to=None
            ticket.save()
            form.save_m2m()
            return redirect("ticket_detail",ticket_id=ticket.pk)

    else:
        form=TicketForm()
    context={
            "form":form
        }
    return render(request,"tickets/create_ticket.html",context)