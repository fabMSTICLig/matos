from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template,render_to_string
from django.template import Context
from django.conf import settings
from django.shortcuts import get_object_or_404
import json
from datetime import datetime

from core.models import Loan, User, Entity, GenericMaterial, SpecificMaterial, SpecificMaterialInstance, LoanGenericItem


class Emails:

    @staticmethod
    def send_status(loan):
        print(loan)
        if(loan.status == Loan.Status.CANCELED):
            status = "annulée"
        elif(loan.status == Loan.Status.REQUESTED):
            status = "en attente"
        elif(loan.status == Loan.Status.ACCEPTED):
            status = "acceptée"
        elif(loan.status == Loan.Status.DENIED):
            status = "refusée"
        context = { 'SITE_URL': settings.SITE_URL, 'loan': loan , 'status': status }
        subject = render_to_string(
            template_name='email/statusloan_subject.txt',
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
        msg = EmailMultiAlternatives(subject, text_content, settings.NOTIFICATION_SENDER, [loan.user.email], reply_to=[loan.entity.contact])
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except:
            print("fail to send notif to "+loan.user.email)
    
    @staticmethod
    def send_manager(loan):

        newloan = loan.status == Loan.Status.REQUESTED
        context = { 'SITE_URL': settings.SITE_URL, 'loan': loan , 'newloan': newloan }

        subject = render_to_string(
            template_name='email/manager_subject.txt',
            context=context
        ).strip()
        text_content = render_to_string(
            template_name='email/manager_message.txt',
            context=context
        )
        html_content = render_to_string(
            template_name='email/manager_message.html',
            context=context
        )
        msg = EmailMultiAlternatives(subject, text_content, settings.NOTIFICATION_SENDER, [loan.entity.contact], reply_to=[loan.user.email])
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except:
            print("fail to send notif to "+loan.entity.contact)
    
    @staticmethod
    def send_extension(loan, date):

        context = { 'SITE_URL': settings.SITE_URL, 'loan': loan , 'date_ext': date }

        subject = render_to_string(
            template_name='email/extension_subject.txt',
            context=context
        ).strip()
        text_content = render_to_string(
            template_name='email/extension_message.txt',
            context=context
        )
        html_content = render_to_string(
            template_name='email/extension_message.html',
            context=context
        )
        msg = EmailMultiAlternatives(subject, text_content, settings.NOTIFICATION_SENDER, [loan.entity.contact], reply_to=[loan.user.email])
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except:
            print("fail to send notif to "+loan.entity.contact)
 
