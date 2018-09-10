from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Model for user-created Profile

    https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

    """
    username = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True
    )
    full_name = models.CharField(max_length=200)
    description = models.TextField()
    avatar = models.ImageField(upload_to='avatars/')

    def __str__(self):
        return str(self.username)


class Skill(models.Model):
    """Model for listing user skills"""
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    skill = models.CharField(max_length=200)

    def __str__(self):
        return self.skill


class GitHub(models.Model):
    """Model for listing user GitHub Projects"""
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    github_project = models.CharField(max_length=200)
    github_url = models.URLField()

    def __str__(self):
        return self.github_project


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
