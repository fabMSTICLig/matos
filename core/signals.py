from django.dispatch import Signal
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Loan
from django.contrib.auth import get_user_model
from django.core.management import call_command

"""
Object Signal listening for event handle_new_loan and handle_status_loan
https://docs.djangoproject.com/fr/3.1/ref/signals/
"""
new_loan = Signal(providing_args=["loan"])
update_status_loan = Signal(providing_args=["loan"])

@receiver(new_loan,sender=Loan)
def handle_new_loan(sender, instance, **kwargs):
    loan = kwargs['loan']
    call_command('notificationsnewloan',id=str(loan.id))

@receiver(update_status_loan,sender=Loan)
def handle_status_loan(sender, status, **kwargs):
    loan = kwargs['loan']
    if(status != 2):
        call_command('notificationstatusloan',id=str(loan.id),status=str(status))
