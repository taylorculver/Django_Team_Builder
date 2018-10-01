from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DeleteView

from . import forms
from . import models


import pdb


def view_project(request, pk):
    """Show individual projects and associated positions"""
    # returns current Project
    project = models.Project.objects.get(id=pk)

    # returns all Positions associated with project
    positions = models.Position.objects.filter(project_id=pk)

    # Returns Applicant Status Form
    application_form = forms.ApplicantStatusForm()

    if request.method == 'POST':
        # FOR DEBUGGING
        # pdb.set_trace()
        # print(request.POST.copy())

        application_form = forms.ApplicantStatusForm(data=request.POST)

        # print(application_form.is_valid())

        if application_form.is_valid():
            application_form.save(commit=False)
            project_id = project.id
            applicant_id = request.user.id

            # https://stackoverflow.com/questions/12698268/additional-post-data-for-django
            position_id = request.POST['position_id']
            models.Applicant.objects.get_or_create(project_id=project_id,
                                                   applicant_id=applicant_id,
                                                   position_id=position_id)

        return redirect('accounts:applications', pk=request.user.id)

    return render(request, 'projects/project.html', {
        'application_form': application_form,
        'pk': pk,
        'project': project,
        'positions': positions,
    })


@login_required
def edit_project(request, pk):
    """Edit individual projects"""
    project = get_object_or_404(models.Project, pk=pk)
    project_form = forms.ProjectForm(instance=project)
    position_formset = forms.PositionFormSet(
        queryset=models.Position.objects.filter(project_id=pk))

    # add prefix's to call each form separately in project_new template
    if request.method == 'POST':
        # FOR DEBUGGING
        # pdb.set_trace()
        # print(request.POST.copy())

        project_form = forms.ProjectForm(data=request.POST)
        position_formset = forms.PositionFormSet(
            data=request.POST,
            queryset=models.Position.objects.all())

        # both forms must be valid to proceed
        if project_form.is_valid() and position_formset.is_valid():

            # must collect logged in userid to ensure
            # referential integrity to User model
            project = project_form.save(commit=False)
            project.owner_id = request.user.id
            models.Project.objects.get_or_create(pk=pk)

            # must collect projectid to ensure
            # referential integrity to the Project model
            positions = position_formset.save(commit=False)
            for position in positions:
                position.project_id = pk
                position.save()

            return redirect('projects:project', pk=pk)

    return render(request, 'projects/project_edit.html', {
        'project_form': project_form,
        'position_formset': position_formset,
        'pk': pk
    })


@login_required
def new_project(request):
    """Create new instances of Project & Position models

    Multiple Forms on Single Page:
    http://www.joshuakehn.com/2013/7/18/multiple-django-forms-in-one-form.html
    https://stackoverflow.com/questions/1395807/proper-way-to-handle-multiple-forms-on-one-page-in-django

    Formsets:
    https://docs.djangoproject.com/en/1.9/topics/forms/formsets/
    https://docs.djangoproject.com/en/1.9/topics/forms/modelforms/#model-formsets

    """

    project_form = forms.ProjectForm(data=request.POST)
    position_formset = forms.PositionFormSet(
        queryset=models.Position.objects.none())

    # add prefix's to call each form separately in project_new template
    if request.method == 'POST':
        # FOR DEBUGGING
        # pdb.set_trace()
        # print(request.POST.copy())

        project_form = forms.ProjectForm(data=request.POST)
        position_formset = forms.PositionFormSet(
            data=request.POST,
            queryset=models.Position.objects.none())

        # both forms must be valid to proceed
        if project_form.is_valid() and position_formset.is_valid():

            # must collect logged in userid to ensure
            # referential integrity to User model
            project = project_form.save(commit=False)
            project.owner_id = request.user.id
            project.save()

            # must collect projectid to ensure
            # referential integrity to the Project model
            positions = position_formset.save(commit=False)
            for position in positions:
                position.project_id = project.id
                position.save()

            return redirect('projects:project', pk=project.pk)

    return render(request, 'projects/project_new.html', {
        'project_form': project_form,
        'position_formset': position_formset
    })


class DiscardProject(DeleteView):
    """
    Discard Existing Projects
    https://docs.djangoproject.com/en/1.9/ref/class-based-views/generic-editing/

    """
    model = models.Project
    success_url = reverse_lazy("home")
