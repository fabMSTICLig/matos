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
