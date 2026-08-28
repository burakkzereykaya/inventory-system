from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import  login_required
from .models import Ticket

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