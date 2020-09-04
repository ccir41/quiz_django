from django.db import models
from django.contrib.auth.models import AbstractUser


def get_profilepicture_path(instance, filename):
    return 'User/{}'.format(filename)


class User(AbstractUser):
    address = models.CharField(max_length=128)
    bio = models.CharField(max_length=300, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=get_profilepicture_path, blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
