from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView,
    TemplateView, UpdateView
)

from . import forms
from . import models


class Project(DetailView):
    """Show individual projects"""
    model = models.Project
    template_name = "projects/project.html"


class EditProject(UpdateView):
    """Edit individual projects"""
    fields = ("name", "owner", "description", "timeline", "requirements")
    model = models.Project
    # template_name_suffix = "_project_edit"


@login_required
def NewProject(request):
    """Create new instances of Project & Position models

    http://www.joshuakehn.com/2013/7/18/multiple-django-forms-in-one-form.html
    https://stackoverflow.com/questions/1395807/proper-way-to-handle-multiple-forms-on-one-page-in-django

    """
    if request.method == "POST":
        # add prefix's to call each form separately in project_new template
        project_form = forms.ProjectForm(request.POST, prefix="project")
        position_form = forms.PositionForm(request.POST, prefix="position")

        # both forms must be valid to proceed
        if project_form.is_valid() and position_form.is_valid():

            # must collect logged in userid to ensure referential integrity to User model
            project = project_form.save(commit=False)
            project.owner_id = request.user.id
            project.save()

            # must collect projectid to ensure referential integrity to the Project model
            position = position_form.save(commit=False)
            position.project_id = project.id
            position.save()
            return redirect('projects:project', pk=project.pk)

    project_form = forms.ProjectForm(prefix="project")
    position_form = forms.PositionForm(prefix="position")
    return render(request, 'projects/project_new.html', {
        'project_form': project_form,
        'position_form': position_form
    })


class DiscardProject(DeleteView):
    """Discard Existing Projects"""
    model = models.Project
    success_url = reverse_lazy("home")
