from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    """Model for user-created project"""
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    description = models.TextField()
    timeline = models.TextField()
    requirements = models.TextField()


class Position(models.Model):
    """Model for positions required on project"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
