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
from django.db import connection

from datetime import datetime

from core.models import Loan, User, Entity, GenericMaterial, SpecificMaterial, SpecificMaterialInstance, LoanGenericItem


class Command(BaseCommand):
    help = 'Send a list of late loans to the entities'

    def handle(self, *args, **options):

        entities = Entity.objects.all()
        for entity in entities:
            loans = Loan.objects.prefetch_related("loangenericitem_set__material").prefetch_related("specific_materials__model").select_related("user").filter(entity=entity).filter(return_date=None).filter(due_date__lt=datetime.today()).filter(status=Loan.Status.ACCEPTED)
            if(len(loans)>0):
                context = { 'SITE_URL': settings.SITE_URL, 'loans': loans, 'entity': entity }
                subject = render_to_string(
                    template_name='emails/lateloans_entities_subject.txt',
                    context=context
                ).strip()
                text_content = render_to_string(
                    template_name='emails/lateloans_entities_message.txt',
                    context=context
                )
                html_content = render_to_string(
                    template_name='emails/lateloans_entities_message.html',
                    context=context
                )
                msg = EmailMultiAlternatives(subject, text_content, settings.NOTIFICATION_SENDER, [entity.contact])
                msg.attach_alternative(html_content, "text/html")
                try:
                    msg.send()
                except:
                    print("fail to send notif to "+entity.contact)
