# tracker/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from django.db import models

# tracker/models.py
from django.db.models.signals import pre_delete
from django.dispatch import receiver


@receiver(pre_delete, sender="tracker.Transaction")
def update_balance_on_delete(sender, instance, **kwargs):
    profile = instance.user.userprofile
    if instance.is_expense:
        profile.balance += instance.amount
    else:
        profile.balance -= instance.amount
    profile.save()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Category(models.Model):
    name = models.CharField(max_length=50)
    is_expense = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank=True)
    date = models.DateField()
    is_expense = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date} - {self.category}: {self.amount}"
