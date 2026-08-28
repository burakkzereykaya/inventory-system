from django import forms
from .models import Ticket,TicketComment

class TicketForm(forms.ModelForm):
    class Meta:
        model=Ticket
        fields=["title","description","priority","affected_devices","affected_location"]

class TicketCommentForm(forms.ModelForm):
    class Meta:
        model=TicketComment
        fields=["comment"]
