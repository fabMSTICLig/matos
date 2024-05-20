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
from django.dispatch import receiver
from django_cas_ng.signals import cas_user_authenticated
from django_auth_ldap.backend import LDAPBackend
from django.conf import settings

@receiver(cas_user_authenticated)
def cas_user_authenticated_callback(sender, **kwargs):
    args = {}
    args.update(kwargs)
    user = LDAPBackend().populate_user(args.get('user').username)
    if user is not None:
        user.is_pro=user.email.endswith(tuple(settings.ISPRO_SCHEMA))
        user.save()
