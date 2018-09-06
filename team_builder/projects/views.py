from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DeleteView

from . import forms
from . import models


def view_project(request, pk):
    """Show individual projects and associated positions"""
    project = models.Project.objects.get(id=pk)
    positions = models.Position.objects.filter(project_id=pk)

    if request.method == 'POST':
        application_form = forms.ApplicationForm(request.POST)

        if application_form.is_valid():
            application = application_form.save(commit=False)
            application.applicant_id = request.user.id
            # bug - positions cannot be hard coded
            application.position_id = 36
            application.project_id = project.id
            application.status = "new"
            application.save()
            return redirect('accounts:applications', pk=request.user.id)

    else:
        application_form = forms.ApplicationForm()

    return render(request, 'projects/project.html', {
        'pk': pk,
        'project': project,
        'positions': positions,
        'application_form': application_form
    })


@login_required
def edit_project(request, pk):
    """Edit individual projects"""
    project = get_object_or_404(models.Project, pk=pk)
    print(project.name)
    position_formset = forms.PositionInlineFormSet(
        queryset=models.Position.objects.filter(project_id=pk)
    )

    # add prefix's to call each form separately in project_new template
    if request.method == 'POST':
        project_form = forms.ProjectForm(request.POST,
                                         prefix="project",
                                         instance=project)
        print(project_form)
        position_formset = forms.PositionInlineFormSet(request.POST,
                                                 prefix="position",
                                                 queryset=models.Position.objects.filter(project_id=pk))

        # both forms must be valid to proceed
        if project_form.is_valid() and position_formset.is_valid():

            # must collect logged in userid to ensure referential integrity to User model
            project = project_form.save(commit=False)
            project.owner_id = request.user.id
            project.save()

            # must collect projectid to ensure referential integrity to the Project model
            positions = position_formset.save(commit=False)
            for position in positions:
                position.project_id = pk
                position.save()
            return redirect('projects:project', pk=pk)

    else:
        project_form = forms.ProjectForm(prefix="project", instance=project)
        position_formset = forms.PositionInlineFormSet(prefix="position",
                                                       queryset=models.Position.objects.filter(project_id=pk))

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
    https://teamtreehouse.com/library/django-forms/inlines-and-media/inline-model-formset

    """
    position_formset = forms.PositionInlineFormSet(
        queryset=models.Position.objects.none()
    )

    # add prefix's to call each form separately in project_new template
    if request.method == 'POST':
        project_form = forms.ProjectForm(request.POST,
                                         prefix="project")
        # print(project_form.is_valid())
        position_formset = forms.PositionInlineFormSet(request.POST,
                                                 prefix="position",
                                                 queryset=models.Position.objects.none())

        # both forms must be valid to proceed
        if project_form.is_valid() and position_formset.is_valid():

            # must collect logged in userid to ensure referential integrity to User model
            project = project_form.save(commit=False)
            project.owner_id = request.user.id
            project.save()

            # must collect projectid to ensure referential integrity to the Project model
            positions = position_formset.save(commit=False)
            for position in positions:
                position.project_id = project.id
                position.save()
            return redirect('projects:project', pk=project.pk)

    else:
        project_form = forms.ProjectForm(prefix="project")
        position_formset = forms.PositionInlineFormSet(prefix="position",
                                                       queryset=models.Position.objects.none())

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
