from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import  login_required
from .models import Ticket, TicketAssignmentHistory
from .forms import TicketForm,TicketCommentForm

@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()

    context={
        "tickets":tickets
    }



    return render(request,"tickets/ticket_list.html",context)

@login_required
def ticket_detail(request, ticket_id):
    comment_form = None
    ticket = get_object_or_404(Ticket,pk=ticket_id)
    comments=ticket.comments.all()
    can_take_ticket= (
        request.user.has_perm("tickets.change_ticket")
        and  ticket.assigned_to is None
        and  ticket.status != Ticket.TicketStatuses.Resolved
    )

    if request.method == "POST":
        if "take_ticket" in request.POST:
            if can_take_ticket:
                ticket.assigned_to=request.user
                ticket.save()

                TicketAssignmentHistory.objects.create(
                    ticket=ticket,
                    previous_assignee=None,
                    new_assignee=request.user,
                    changed_by=request.user,
                )

                return redirect("ticket_detail",ticket_id=ticket.pk)

        else:
                    if request.user.has_perm("tickets.add_ticketcomment"):
                            comment_form=TicketCommentForm(request.POST)
                            if comment_form.is_valid():
                                comment=comment_form.save(commit=False)
                                comment.ticket=ticket
                                comment.author=request.user
                                comment.save()

                                return redirect("ticket_detail",ticket_id=ticket.pk)
                    else:
                        comment_form = None


    else:
        if request.user.has_perm("tickets.add_ticketcomment"):
            comment_form= TicketCommentForm()


    context = {
    "ticket": ticket,
    "comments": comments,
   "comment_form": comment_form,
    "can_take_ticket": can_take_ticket
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