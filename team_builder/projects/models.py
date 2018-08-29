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

    def __str__(self):
        return self.name


class Position(models.Model):
    """Model for positions required on project"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class Application(models.Model):
    """Model for applications to a position"""
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.id
