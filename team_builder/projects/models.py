from django.core.urlresolvers import reverse
from django.db import models


class Project(models.Model):
    """Model for user-created project"""
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    description = models.TextField()
    timeline = models.TextField()
    requirements = models.TextField()

    # def get_absolute_url(self):
    #     # Needed for creation of new project
    #     return reverse("projects:project", kwargs={"pk": self.pk})


# class Position(models.Model):
#     """Model for positions required on project"""
#     project = models.ForeignKey(
#         Project,
#         on_delete=models.CASCADE,
#         verbose_name="id"
#     )
#     title = models.CharField(max_length=200)
#     description = models.TextField()
