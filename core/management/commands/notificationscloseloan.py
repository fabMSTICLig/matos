from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template,render_to_string
from django.template import Context
from django.conf import settings
from django.db.models import Q

import datetime

from core.models import Loan, User, Entity, GenericMaterial, SpecificMaterial, SpecificMaterialInstance, LoanGenericItem


class Command(BaseCommand):
    help = 'Send notification for close due date'

    def handle(self, *args, **options):
        weeknot = datetime.datetime.today()+datetime.timedelta(days=7)
        midweeknot = datetime.datetime.today()+datetime.timedelta(days=3)
        daybeforenot = datetime.datetime.today()+datetime.timedelta(days=1)
        loans = Loan.objects.filter(return_date=None).filter(Q(due_date=weeknot)|Q(due_date=midweeknot)|Q(due_date=daybeforenot)).filter(status=3)

        for loan in loans:
            context = { 'SITE_URL': settings.SITE_URL, 'loan': loan }
            subject = render_to_string(
                template_name='email/closeloan_subject.txt',
                context=context
            ).strip()
            text_content = render_to_string(
                template_name='email/closeloan_message.txt',
                context=context
            )
            html_content = render_to_string(
                template_name='email/closeloan_message.html',
                context=context
            )
            msg = EmailMultiAlternatives(subject, text_content, settings.NOTIFICATION_SENDER, [loan.user.email], reply_to=settings.NOTIFICATION_REPLYTO)
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                print("fail to send notif to "+loan.user.email)
