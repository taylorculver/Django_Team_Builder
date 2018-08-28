from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html


class Profile(models.Model):
    """Model for user-created Profile"""
    username = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=200)
    description = models.TextField()
    avatar = models.ImageField(upload_to='avatars/')

    # def save(self, *args, **kwargs):
    #     """Returns the first_name plus the last_name, with a space in between."""
    #     if User.first_name or User.last_name is None:
    #         self.full_name = ""
    #     else:
    #         self.full_name = '%s %s' % (User.first_name, User.last_name)
    #     super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


# from accounts.models import Skill -- to use in Python Shell
class Skill(models.Model):
    """Model for listing user skills"""
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    skill = models.CharField(max_length=200)

    def __str__(self):
        return self.skill


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
