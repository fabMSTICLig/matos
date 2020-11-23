from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template,render_to_string
from django.template import Context
from django.conf import settings

from datetime import datetime

from core.models import Loan, User, Entity, GenericMaterial, SpecificMaterial, SpecificMaterialInstance, LoanGenericItem


class Command(BaseCommand):
    help = 'Send notification for late return and approching return'

    def add_arguments(self, parser):
        parser.add_argument('--return', '-r', default=None, dest='return', action='append',
                            help='add option return')

    def handle(self, *args, **options):
        loans = Loan.objects.filter(return_date=None).filter(due_date__gt=datetime.today()).filter(status=3)
        late = False

        if options['return']:
            print("opt=return")
            loans = Loan.objects.filter(return_date__lt=datetime.today()).filter(status=3)
            late = True

        for loan in loans:
            context = { 'SITE_URL': settings.SITE_URL, 'loan': loan, 'late': late }
            subject = render_to_string(
                template_name='email/lateloan_subject.txt',
                context=context
            ).strip()
            text_content = render_to_string(
                template_name='email/lateloan_message.txt',
                context=context
            )
            html_content = render_to_string(
                template_name='email/lateloan_message.html',
                context=context
            )
            msg = EmailMultiAlternatives(subject, text_content, settings.NOTIFICATION_SENDER, [loan.user.email])
            msg.attach_alternative(html_content, "text/html")
            print(msg.message())
            #msg.send()
