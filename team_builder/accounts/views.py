from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import mail
from django.core.urlresolvers import reverse
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render, redirect

from . import models
from . import forms
from .apps import Project, Position, Applicant


def sign_in(request):
    """Default Sign In View for Django Application"""
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:profile', args=[user.id])
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/signin.html', {'form': form})


def sign_up(request):
    """Default Sign Up View for for Django application"""
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse(
                'accounts:profile', args=[user.id]))
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def sign_out(request):
    """Default Sign Out view for Django application"""
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('accounts:sign_in'))


@login_required
def view_profile(request, pk):
    """Show User Profile, associated Projects and Skills"""
    # query current logged in User
    user = models.User.objects.get(id=pk)

    # query all Projects associated with logged in User
    projects = Project.objects.filter(owner_id=pk)

    # query all Skills associated with logged in User's Profile
    skills = models.Skill.objects.filter(profile_id=models.Profile.objects.get(username_id=pk).id)
    return render(request, "accounts/profile.html", {
        'pk': pk,
        'user': user,
        'projects': projects,
        'skills': skills
    })


@login_required
def edit_profile(request, pk):
    """Edit User Profile"""
    user = models.User.objects.get(pk=pk)
    projects = Project.objects.filter(owner_id=pk)
    profile = models.Profile.objects.get(username_id=pk)

    # BUG when posting multiple formset forms

    skills_formset = inlineformset_factory(models.Profile, models.Skill, fields=('skill',), max_num=1, can_delete=False)
    profile_form = forms.ProfileForm(instance=user.profile)

    if request.method == 'POST':
        profile_form = forms.ProfileForm(instance=user.profile,
                                         data=request.POST,
                                         files=request.FILES)

        skills_formset = skills_formset(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid() and skills_formset.is_valid():
            profile_form.save()
            skills_formset.save()
            return redirect('accounts:profile', pk=pk)

    return render(request, 'accounts/profile_edit.html', {
        'profile_form': profile_form,
        'pk': pk,
        'projects': projects,
        'skills_formset': skills_formset
    })


@login_required
def view_applications(request, pk):
    """See all of the Applicants for my Project's Position(s)"""

    """PROJECT RELATED QUERIES"""
    # query all Project(s) that belong to current logged in User
    my_projects = Project.objects.filter(owner_id=pk).values()

    # build list of all Project id's belonging to current logged in User
    my_project_ids = [ids['id'] for ids in my_projects]

    """POSITION RELATED FILTERING"""
    # query all Positions associated with my Projects
    my_positions = Position.objects.filter(project_id__in=my_project_ids)

    """STATUS RELATED FILTERING"""
    # canned variables for Applicant(s) status
    statuses = ["New", "Accepted", "Rejected"]

    """ASSEMBLE FINAL FILTER"""
    # query list of all Applicant(s) who have applied to current User's Project(s)
    queryset = Applicant.objects.filter(project_id__in=my_project_ids)

    # join related Applicant and Position models to Applicant(s) who have applied to current User's Project(s)
    joined_queryset = queryset.select_related("applicant").select_related("position")

    # return values for Applicant, id, full name, position title, project name, and status to return to view
    applicants = joined_queryset.values('applicant_id',
                                        'applicant__full_name',
                                        'position__title',
                                        'project__name',
                                        'status'
                                        )

    if request.method == 'POST':
        # bug - positions cannot be hard coded
        application = Applicant.objects.get(position_id=36,
                                            project_id=41,
                                            applicant_id=request.user.id
                                            )
        application_form = forms.ApplicantStatusForm(request.POST)

        if application_form.is_valid():
            if application.status == "new":
                application.status = "approved"
            elif application.status == "approved":
                application.status = "rejected"
            elif application.status == "rejected":
                application.status = "approved"
            print(application.status)
            # bug - positions cannot be hard coded
            Applicant.objects.update(position_id=36,
                                     project_id=41,
                                     status=application.status,
                                     applicant_id=request.user.id
                                     )

            connection = mail.get_connection()

            # Manually open the connection
            connection.open()

            # Construct an email message that uses the connection
            email = mail.EmailMessage(
                subject='Regarding Your Application',
                body="Your application to blah was {}".format(application.status),
                from_email='from@teambuilder.com',
                to=['to@applicant.com'],
                connection=connection,
            )
            email.send()  # Send the email

            # We need to manually close the connection.
            connection.close()

            return redirect('accounts:applications', pk=request.user.id)

    return render(request, "accounts/applications.html", {
        'pk': pk,
        'applicants': applicants,
        'my_positions': my_positions,
        'my_projects': my_projects,
        'statuses': statuses
    })


@login_required
def filter_applications(request, pk, filter):
    """Filter for all of the Applicants for my Project's Position(s)"""

    """PROJECT RELATED FILTERING"""
    # query all Project(s) that belong to current logged in User
    my_projects = Project.objects.filter(owner_id=pk).values()

    # build list of all Project id's belonging to current logged in User
    my_project_ids = [ids['id'] for ids in my_projects]

    # filter for all Project(s) that the current User is associated with
    my_filtered_projects = Project.objects.filter(Q(owner_id=pk) & Q(name__icontains=filter)).values()

    # build list of all Project id's belonging to current logged in User w/ filters applied
    my_filtered_project_ids = [ids['id'] for ids in my_filtered_projects]

    """POSITION RELATED FILTERING"""
    # query all Positions associated with my Projects
    my_positions = Position.objects.filter(project_id__in=my_project_ids)

    # filter for all Positions(s) that the current User is associated with
    my_filtered_positions = Position.objects.filter(title__icontains=filter).values()

    # build list of all Position id's belonging to current logged in User w/ filters applied
    my_filtered_position_ids = [ids['id'] for ids in my_filtered_positions]

    """STATUS RELATED FILTERING"""
    # canned variables for Applicant(s) status
    statuses = ["New", "Accepted", "Rejected"]

    """ASSEMBLE FINAL FILTER"""
    # query list of all Applicant(s) who have applied to current User's Project(s)
    queryset = Applicant.objects.filter(
        Q(project_id__in=my_filtered_project_ids) |
        Q(position_id__in=my_filtered_position_ids) |
        Q(status=filter)
    )

    # join related Applicant and Position models to Applicant(s) who have applied to current User's Project(s)
    joined_queryset = queryset.select_related("applicant").select_related("position")

    # return values for Applicant, id, full name, position title, project name, and status to return to view
    applicants = joined_queryset.values('applicant_id',
                                        'applicant__full_name',
                                        'position__title',
                                        'project__name',
                                        'status'
                                        )

    return render(request, "accounts/applications.html", {
        'pk': pk,
        'applicants': applicants,
        'my_positions': my_positions,
        'my_projects': my_projects,
        'statuses': statuses
    })

