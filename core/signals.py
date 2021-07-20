from django.dispatch import receiver
from django_cas_ng.signals import cas_user_authenticated
from django_auth_ldap.backend import LDAPBackend

@receiver(cas_user_authenticated)
def cas_user_authenticated_callback(sender, **kwargs):
    args = {}
    args.update(kwargs)
    user = LDAPBackend().populate_user(args.get('user'))
    if user is not None:
        user.save()
