from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from channels import Group

# Create your models here.


class Theatre(models.Model):
    owner = models.ForeignKey('auth.User', related_name='theatres', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    youtube_url = models.CharField(max_length=255, blank=False, unique=True)

    def __str__(self):
        return "{}".format(self.name)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
