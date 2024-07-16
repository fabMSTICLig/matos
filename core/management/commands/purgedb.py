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
from django.conf import settings
from django.db.models import Q

import datetime

from core.models import Loan, User


class Command(BaseCommand):
    help = 'Purge the database from old loan and inactive users'

    def handle(self, *args, **options):
        purgedate = datetime.date.fromisoformat(settings.PURGE_DATE)
        purgedate = purgedate.replace(year = datetime.date.today().year-purgedate.year)
        print(purgedate)
        print(Loan.objects.filter(return_date__lte = purgedate).delete())
        print(User.objects.filter(last_login__lte = purgedate).filter(loans=None).delete())
