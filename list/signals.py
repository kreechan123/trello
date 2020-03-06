from .models import BoardMember, Board
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Board)
def add_board_member(sender, instance, created, **kwargs):
    if created:
        user_member = BoardMember(member=instance.owner,board=instance)
        user_member.save()