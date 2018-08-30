from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import CharField, inlineformset_factory, modelform_factory, Textarea
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, FormView,
    TemplateView, UpdateView
)
from django.views.generic.edit import FormMixin

from . import forms
from . import models


def project_view(request, pk):
    """Show individual projects and associated positions"""
    project = models.Project.objects.get(id=pk)
    positions = models.Position.objects.filter(project_id=pk)

    # application_form = forms.ApplicationForm()
    # application_form.fields['applicant'].initial = request.user.id

    if request.method == 'POST':
        application_form = forms.ApplicationForm(request.POST)
        print(application_form)
        print(application_form.is_valid())

        if application_form.is_valid():
            application = application_form.save(commit=False)
            application.applicant_id = request.user.id
            application.position_id = 36
            application.status = "applied"
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

# class Project(FormMixin,  DetailView):
#     """
#     Show individual projects and associated positions
#
#     Get Context Data for Second Model:
#     https://docs.djangoproject.com/en/1.9/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_data
#
#     Obtain Postions Associated with Project Primary Key:
#     https://stackoverflow.com/questions/25881015/django-queryset-return-single-value
#
#     """
#     queryset = models.Project.objects.all()
#     template_name = "projects/project.html"
#     context_object_name = "project"
#
#     def get_context_data(self, **kwargs):
#         context = super(Project, self).get_context_data(**kwargs)
#         context['positions'] = models.Position.objects.filter(project_id=self.kwargs['pk'])
#         return context
#
#     # def post(self, request, *args, **kwargs):
#     #     context = super(Project, self).get_context_data(**kwargs)
#     #     context['applications'] = models.Application.objects.filter(applicant_id=self.kwargs['pk'])
#     #     if context["form"].is_valid():
#     #         print("yes done")
#     #     return super(DetailView, self).render_to_response(context)

@login_required
def EditProject(request, pk):
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
def NewProject(request):
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


# @login_required
class DiscardProject(DeleteView):
    """
    Discard Existing Projects
    https://docs.djangoproject.com/en/1.9/ref/class-based-views/generic-editing/

    """
    model = models.Project
    success_url = reverse_lazy("home")
