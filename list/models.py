import os, uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# from list.models import Boardlist, Board, BoardMember, Card, Profile, User, CardComment

def avatar(instance, filename):
    return '/'.join(['avatars', instance.board.board.title, filename])
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.FileField(upload_to=avatar, blank=True, null=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
    

class Board(models.Model):
    """Board Model
    """
    title = models.CharField(max_length=200)
    archive = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Boardlist(models.Model):
    """Boardlist Model
    """
    title = models.CharField(max_length=200)    
    archived = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


def uploadto(instance, filename):
    return '/'.join(['uploads', instance.board.board.title, filename])


class Card(models.Model):
    """ Card Model
    """
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=200, blank=True, null=True)
    image = models.FileField(upload_to=uploadto, blank=True, null=True)
    card_image_name = models.CharField(max_length=128, blank=True, null=True)
    board = models.ForeignKey(Boardlist, on_delete=models.CASCADE, null=False)
    position = models.PositiveIntegerField(default=0)
    #group = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def get_image_name(self):
        return self.image.name


class BoardMember(models.Model):
    """BoardMember Model
    """
    board = models.ForeignKey(Board,on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    member = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank="True")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class Invite(models.Model):
    """Invite Model
    """
    token = models.UUIDField(default=uuid.uuid4, editable=False) 
    email = models.EmailField(max_length=254)
    board = models.ForeignKey(Board,on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank="True")
    date_invited = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

class CardComment(models.Model):
    """CardComment Model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank="True")
    comment = models.TextField(max_length=200, blank=True, null=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE,null=True, blank="True")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)