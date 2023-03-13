from .models import Loan, User, Entity, GenericMaterial, SpecificMaterial, SpecificMaterialInstance, LoanGenericItem
import datetime
from django.http import HttpResponse
from pathlib import Path
from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template,render_to_string
from django.template import Context
import time
from django import template
from django.conf import settings

class AlertLoansEnded(CronJobBase):
    """
    récuperation des prêts arrivés à terme
    """
    schedule = Schedule(run_every_mins=0)
    code = 'core.cron.alert_loans_ended'    # a unique code

    def get_rendered_template(self, tpl, context):
        return self.get_template(tpl).render(context)


    def get_template(self, tpl):
        return template.loader.get_template(tpl)

    ## récuperation des reservations
    def do(self):
        loans = Loan.objects.all()
        year = datetime.date.today().year
        month = datetime.date.today().month
        day = datetime.date.today().day
        date_format = "%Y-%m-%d"
        now = datetime.datetime.strptime(str(year)+"-"+str(month)+"-"+str(day), date_format)
        loansEnded = {}
        for loan in loans:
            due_date = datetime.datetime(loan.due_date.year,loan.due_date.month,loan.due_date.day)
            if((now >= due_date) and loan.status == 3 and loan.return_date is None):
                item = {}
                item["id"] = loan.pk
                item["genericmaterials"] = []
                item["specificinstances"] = []
                item["entity"] = loan.entity
                item["checkout_date"] = loan.checkout_date
                item["due_date"] =  loan.due_date
                for mat in loan.generic_materials.all():
                    item["genericmaterials"].append({"name": mat.name,"quantity":mat.quantity})
                for mat in loan.specific_materials.all():
                    item["specificinstances"].append({"name": mat.name,"serial_num":mat.serial_num})
                if not loan.user.email in loansEnded:
                    loansEnded[loan.user.email]=[item]

                else:
                    loansEnded[loan.user.email].append(item)

        for i,x in enumerate(loansEnded):
            for loans in loansEnded[x]:
                html_tpl  = get_template('email/loans.html')
                context = { 'loans': loans }
                html_content = self.get_rendered_template('email/loans.html', context)
                from_email = 'mail'
                to = [x,] # put your real email here
                subject = 'Plateforme MATOS : prêts en retard'
                text_content = 'liste des prêts à retourner'
                msg=EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

class AlertLoansDueDate(CronJobBase):
    """
    récuperation des prêts arrivant à échéance
    """
    schedule = Schedule(run_every_mins=0)
    code = 'core.cron.alert_loans_due_date'    # a unique code


    def get_rendered_template(self, tpl, context):
        return self.get_template(tpl).render(context)

    def get_template(self, tpl):
        return template.loader.get_template(tpl)

    ## récuperation des reservations


    def do(self):
        year = datetime.date.today().year
        month = datetime.date.today().month
        day = datetime.date.today().day

        date_format = "%Y-%m-%d"
        now = datetime.datetime.strptime(str(year)+"-"+str(month)+"-"+str(day), date_format)

        loans_to_end = []
        loans = Loan.objects.all()
        return_loans = {}

        for loan in loans:
            due_date = datetime.datetime(loan.due_date.year, loan.due_date.month, loan.due_date.day)
            if((now <= due_date) and loan.status == 3 and loan.return_date is None):
                if((due_date - now).days <= 1):
                    if not loan.user.email in return_loans:
                        due_time={}
                        due_time["day"]=[loan.id]
                        return_loans[loan.user.email]=due_time
                    else:
                        if "day" in return_loans[loan.user.email]:
                            #return_loans[loan.user.email][x].append(loan.id)
                            print("append")
                        else:
                            due_time={}
                            due_time["day"] = [loan.id]
                            return_loans[loan.user.email]["day"]=[loan.id]

                elif((due_date - now).days > 1 and (due_date - now).days <= 4):
                    if not loan.user.email in return_loans:
                        due_time={}
                        due_time["midweek"]=[loan.id]
                        return_loans[loan.user.email]=due_time

                    else:
                        if "midweek" in return_loans[loan.user.email] :
                            print("append")
                            #return_loans[loan.user.email][x].append(loan.id)
                        else:
                            return_loans[loan.user.email]["midweek"]=[loan.id]

                elif((due_date - now).days > 4 and (due_date - now).days <= 7):
                    if not loan.user.email in return_loans:
                        due_time = {}
                        due_time["week"] = [loan.id]
                        return_loans[loan.user.email]=due_time

                    else:
                        if "week" in return_loans[loan.user.email]:
                                #return_loans[loan.user.email][x].append(loan.id)
                                print("append")

                        else:
                            return_loans[loan.user.email]["week"]=[loan.id]
        if(len(return_loans) > 0):
            for borrower in return_loans:
                #loan = Loan.objects.get(pk=id)
                for next_return in return_loans[borrower]:
                    for i, loan in enumerate(return_loans[borrower][next_return]):
                        obj = Loan.objects.get(pk=loan)
                        item = {}
                        item["id"] = loan
                        item["genericmaterials"] = []
                        item["specificinstances"] = []
                        item["entity"] = obj.entity
                        item["checkout_date"] = obj.checkout_date
                        for mat in obj.generic_materials.all():
                            item["genericmaterials"].append({"name": mat.name,"quantity":mat.quantity})
                        for mat in obj.specific_materials.all():
                            item["specificinstances"].append({"name": mat.name,"serial_num":mat.serial_num})
                        return_loans[borrower][next_return][i]=item

                    context = { 'loans': return_loans[borrower][next_return], 'delta':next_return }
                    html_content = self.get_rendered_template('email/loans.html', context)
                    from_email = 'email'
                    to = [borrower,] # put your real email here
                    subject = 'Plateforme MATOS : prêts arrivant à échéance'
                    text_content = 'liste des emprunts à retourner'
                    msg=EmailMultiAlternatives(subject, text_content, from_email, to)
                    msg.attach_alternative(html_content, "text/html")
                    print(msg)
                    msg.send()
