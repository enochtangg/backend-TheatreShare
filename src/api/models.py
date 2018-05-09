from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from channels import Group
from django.utils.six import python_2_unicode_compatible
from .settings import MSG_TYPE_MESSAGE

import json

# Create your models here.


@python_2_unicode_compatible
class Theatre(models.Model):
    owner = models.ForeignKey('auth.User', related_name='theatres', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    youtube_url = models.CharField(max_length=255, blank=False, unique=True)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.name)

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("theatre-%s" % self.id)

    def send_message(self, message, user, action, msg_type=MSG_TYPE_MESSAGE):
        """
        Called to send a message to the room on behalf of a user.
        """
        final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type, 'action': action}

        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
