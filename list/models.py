import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# from list.models import Boardlist, Board, BoardMember, Card


class Board(models.Model):
    title = models.CharField(max_length=200)
    archive = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Boardlist(models.Model):
    title = models.CharField(max_length=200)    
    archived = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

class BoardMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    board = models.ForeignKey(Board,on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)



def uploadto(instance, filename):
    return '/'.join([filename])

class Card(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=200, blank=True, null=True)
    image = models.FileField(upload_to=uploadto, blank=True, null=True)
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