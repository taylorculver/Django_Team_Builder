from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models

from accounts.models import Profile


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
    # url = models.TextField()

    def __str__(self):
        return self.name


class Position(models.Model):
    """Model for positions required on project"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class Applicant(models.Model):
    """Model for applications to a position"""
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        to_field="username_id"
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=200, default="new")
    reverse_status = models.CharField(max_length=200, default="approved")

    def save(self, *args, **kwargs):
        if self.status == "new":
            self.reverse_status = "approved"
        elif self.status == "approved":
            self.reverse_status = "rejected"
        elif self.status == "rejected":
            self.reverse_status = "approved"
        super(Applicant, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.applicant_id)
