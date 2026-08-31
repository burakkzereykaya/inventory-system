from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import  login_required
from .models import Ticket, TicketAssignmentHistory,TicketStatusHistory
from .forms import TicketForm,TicketCommentForm,TicketStatusForm
from django.contrib import messages
from django.utils import timezone

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
    status_form =None
    ticket = get_object_or_404(Ticket,pk=ticket_id)
    comments=ticket.comments.all()
    status_history=(
               ticket.ticket_status_history
               .all()
               .order_by("-changed_at")
    )
    assignment_history=(
        ticket.ticket_assignment_history
        .all()
        .order_by("changed-at")
    )
    can_update_status = (
            request.user.is_superuser
            or (
                    request.user.has_perm("tickets.change_ticket")
                    and ticket.assigned_to == request.user
            )
    )
    if can_update_status:
        status_form = TicketStatusForm(instance=ticket)

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

                messages.success(request,"Ticket successfully assigned to you.")

                return redirect("ticket_detail",ticket_id=ticket.pk)
            else:
                messages.warning(request,"This ticket can not be taken.")
                return redirect("ticket_detail", ticket_id=ticket.pk)

        elif "update_status" in request.POST:
            if can_update_status:
                status_form = TicketStatusForm(
                    request.POST,
                    instance=ticket
                )

                previous_status=ticket.status


                if status_form.is_valid():
                    updated_ticket = status_form.save(commit=False)
                    new_status = updated_ticket.status
                    if previous_status != new_status:
                        if new_status == Ticket.TicketStatuses.Resolved:
                            updated_ticket.resolved_at=timezone.now()

                        updated_ticket.save()
                        TicketStatusHistory.objects.create(
                                ticket=updated_ticket,
                                previous_status=previous_status,
                                new_status=new_status,
                                changed_by=request.user,)


                        messages.success(request,"Ticket status changed successfully.")

                        return redirect("ticket_detail",ticket_id=ticket.pk)

                    else:
                        messages.info(request,"Ticket status has not changed.")

                        return redirect("ticket_detail",ticket_id=ticket.pk)


        else:
            if request.user.has_perm("tickets.add_ticketcomment"):
                comment_form=TicketCommentForm(request.POST)
                if comment_form.is_valid():
                    comment=comment_form.save(commit=False)
                    comment.ticket=ticket
                    comment.author=request.user
                    comment.save()

                    messages.success(request,"Comment added successfully.")

                    return redirect("ticket_detail",ticket_id=ticket.pk)


    else:
        if request.user.has_perm("tickets.add_ticketcomment"):
            comment_form= TicketCommentForm()


    context = {
    "ticket": ticket,
    "comments": comments,
    "comment_form": comment_form,
    "can_take_ticket": can_take_ticket,
    "status_form":status_form,
    "status_history":status_history,
    "assignment_history":assignment_history,
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