from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template,render_to_string
from django.template import Context
from django.conf import settings

from datetime import datetime

from core.models import Loan, User, Entity, GenericMaterial, SpecificMaterial, SpecificMaterialInstance, LoanGenericItem


class Command(BaseCommand):
    help = 'Send notification for new requested loan'

    def add_arguments(self, parser):
        parser.add_argument('--id', '-id', default=None, dest='id', action='append',
                            help='set id of new loan')

    def handle(self, *args, **options):
        if(options['id']):
            print(options['id'])
            loan = Loan.objects.get(pk=options['id'])

            email_entity = Entity.objects.get(pk=loan.entity.id)

            context = { 'SITE_URL': settings.SITE_URL, 'loan': loan }
            subject = render_to_string(
                template_name='email/newloan_subject.txt',
                context=context
            ).strip()
            text_content = render_to_string(
                template_name='email/newloan_message.txt',
                context=context
            )
            html_content = render_to_string(
                template_name='email/newloan_message.html',
                context=context
            )
            msg = EmailMultiAlternatives(subject, text_content, settings.NOTIFICATION_SENDER, [email_entity.contact])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                print("fail to send notif to "+email_entity.contact)
