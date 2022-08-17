import os

from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.models import Profile


@receiver(pre_save, sender=Profile)
def my_handler(sender, instance,update_fields, **kwargs):
    if instance.pk and instance.avatar:
        old_profile = sender.objects.get(id=instance.pk)
        if old_profile.avatar and instance.avatar != old_profile.avatar:
            old_img = old_profile.avatar.path
            if os.path.exists(old_img):
                os.remove(old_img)
