# tracker/signals.py
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Transaction


@receiver(pre_delete, sender=Transaction)
def update_balance_on_delete(sender, instance, **kwargs):
    profile = instance.user.userprofile
    if instance.is_expense:
        profile.balance += instance.amount
    else:
        profile.balance -= instance.amount
    profile.save()
