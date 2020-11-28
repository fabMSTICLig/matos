from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template,render_to_string
from django.template import Context
from django.conf import settings
from django.shortcuts import get_object_or_404
import json
from datetime import datetime

from core.models import Loan, User, Entity, GenericMaterial, SpecificMaterial, SpecificMaterialInstance, LoanGenericItem


class Command(BaseCommand):
    help = 'Send notification for status changes'

    def add_arguments(self, parser):
        parser.add_argument('--id', '-id', default=None, dest='id', action='append',
                            help='set id of loan')
        parser.add_argument('--status', '-status', default=None, dest='status', action='append',
                            help='set status of loan')

    def handle(self, *args, **options):
        if(options['id']) and (options['status']):
            loan = Loan.objects.get(pk=options['id'])
            tpl_name=''
            if(options['status'] == '3'):
                tpl_name = 'valide'
            if(options['status'] == '4'):
                tpl_name = 'reject'
            if(options['status'] == '1'):
                tpl_name = 'cancel'

            context = { 'SITE_URL': settings.SITE_URL, 'loan': loan , 'status': options['status']}
            subject = render_to_string(
                template_name='email/'+tpl_name+'loan_subject.txt',
                context=context
            ).strip()
            text_content = render_to_string(
                template_name='email/statusloan_message.txt',
                context=context
            )
            html_content = render_to_string(
                template_name='email/statusloan_message.html',
                context=context
            )
            msg = EmailMultiAlternatives(subject, text_content, settings.NOTIFICATION_SENDER, [loan.user.email])
            msg.attach_alternative(html_content, "text/html")
            print(msg.message())
            #msg.send()
            print('email envoyé')
