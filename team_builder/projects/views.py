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


# class based view used originally, but moved to model form to handle custom HTML templates
# class NewProject(CreateView):
#     """Create new projects"""
#     fields = ("name", "description", "timeline", "requirements")
#     model = models.Project


# @login_required
def NewProject(request):
    """Create new instances of Project model"""
    if request.method == "POST":
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('projects:project', pk=project.pk)

    form = forms.ProjectForm()
    # print(form)
    return render(request, 'projects/project_new.html', {'form': form})


class DiscardProject(DeleteView):
    """Discard Existing Projects"""
    model = models.Project
    success_url = reverse_lazy("home")
