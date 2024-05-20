"""
Copyright (C) 2020-2024 LIG Université Grenoble Alpes


This file is part of Matos.

Matos is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
@author Clément Lesaulnier
@author Robin Courault
"""
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
                template_name='emails/endingloan_subject.txt',
                context=context
            ).strip()
            text_content = render_to_string(
                template_name='emails/endingloan_message.txt',
                context=context
            )
            html_content = render_to_string(
                template_name='emails/endingloan_message.html',
                context=context
            )
            msg = EmailMultiAlternatives(subject, text_content, settings.NOTIFICATION_SENDER, [loan.user.email], reply_to=settings.NOTIFICATION_REPLYTO)
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                print("fail to send notif to "+loan.user.email)
