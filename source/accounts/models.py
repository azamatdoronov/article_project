from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, BaseValidator
from django.db import models

# Create your models here.
from django.utils.deconstruct import deconstructible


def get_url_path(instance, filename):
    # print(instance)
    # print(filename)
    return f"avatars/{instance.user.pk}/{filename}"


@deconstructible
class FileSizeValidator(BaseValidator):
    code = "invalid_filesize"

    def compare(self, a, b):
        return a > b * 1024 * 1024

    def clean(self, x):
        return len(x)


class Profile(models.Model):
    birthday = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    avatar = models.ImageField(upload_to=get_url_path, null=True, blank=True, verbose_name="Аватар",
                               validators=[
                                   FileExtensionValidator(['jpg', 'jpeg'], "Файлы только jpg и jpeg"),
                                   FileSizeValidator(limit_value=5)
                               ]
                               )
    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                verbose_name="Пользователь",
                                related_name="profile")
