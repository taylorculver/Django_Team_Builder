from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404


import pdb

from . import models
from . import forms
from .apps import Project, Position, Applicant


def send_email(application):
    """Function to send email upon rejection or acceptance"""
    connection = mail.get_connection()

    # Manually open the connection
    connection.open()

    project = Project.objects.get(pk=application.project_id)
    status = application.status
    full_name = models.Profile.objects.get(username_id=application.applicant_id).full_name

    # Construct an email message that uses the connection
    """https://docs.djangoproject.com/en/1.9/topics/email/#emailmessage-objects"""
    email = mail.EmailMessage(
        subject='Hi {}, Regarding Your Application'.format(full_name),
        body="Your application to {} was {}. Thank you for using the team builder application!".format(project, status),
        from_email='from@teambuilder.com',
        to=['to@applicant.com'],
        connection=connection,
    )
    email.send()  # Send the email

    # We need to manually close the connection.
    connection.close()


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

    # query all GitHub Projects associated with logged in User's Profile
    githubs = models.GitHub.objects.filter(profile_id=models.Profile.objects.get(username_id=pk).id)

    return render(request, "accounts/profile.html", {
        'githubs': githubs,
        'pk': int(pk),
        'projects': projects,
        'user': user,
        'skills': skills
    })


@login_required
def edit_profile(request, pk):
    """Edit User Profile"""
    # obtain current logged in User
    user = models.User.objects.get(pk=pk)

    # obtain all Project(s) for logged in User
    projects = Project.objects.filter(owner_id=pk)

    # obtain associated Profile for logged in User
    profile = get_object_or_404(models.Profile, username_id=pk)

    # generate Skills Formset
    skills_formset = forms.SkillFormSet(queryset=profile.skill_set.all(),
                                        # prefix required for multiple formsets on a single page
                                        prefix='skills_formset')

    # generate GitHub Formset
    github_formset = forms.GitHubFormSet(queryset=profile.github_set.all(),
                                         # prefix required for multiple formsets on a single page
                                         prefix='github_formset')

    # generate Profile form
    profile_form = forms.ProfileForm(instance=user.profile)

    if request.method == 'POST':
        # FOR DEBUGGING
        # pdb.set_trace()
        # print(request.POST.copy())

        profile_form = forms.ProfileForm(instance=user.profile,
                                         data=request.POST,
                                         # files are necessary since we're sending over an image
                                         files=request.FILES)

        skills_formset = forms.SkillFormSet(request.POST,
                                            queryset=profile.skill_set.all(),
                                            # prefix required for multiple formsets on a single page
                                            prefix='skills_formset',
                                            )

        github_formset = forms.GitHubFormSet(request.POST,
                                             queryset=profile.github_set.all(),
                                             # prefix required for multiple formsets on a single page
                                             prefix='github_formset'
                                             )

        if profile_form.is_valid() and skills_formset.is_valid() and github_formset.is_valid():
            profile_form.save()

            skills = skills_formset.save(commit=False)
            for skill in skills:
                # associate each Skill with a User's Profile
                skill.profile_id = profile.id
                skill.save()

            githubs = github_formset.save(commit=False)
            for github in githubs:
                # associate each Github with a User's Profile
                github.profile_id = profile.id
                github.save()

        return redirect('accounts:profile', pk=pk)

    return render(request, 'accounts/profile_edit.html', {
        'github_formset': github_formset,
        'pk': pk,
        'profile_form': profile_form,
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
    statuses = ["New", "Approved", "Rejected"]

    """ASSEMBLE FINAL FILTER"""
    # query list of all Applicant(s) who have applied to current User's Project(s)
    queryset = Applicant.objects.filter(project_id__in=my_project_ids)

    # join related Applicant and Position models to Applicant(s) who have applied to current User's Project(s)
    joined_queryset = queryset.select_related("applicant").select_related("position")

    # return values for Applicant, id, full name, position title, project name, and status to return to view
    applicants = joined_queryset.values('applicant_id',
                                        'id',
                                        'applicant__full_name',
                                        'position__title',
                                        'project__name',
                                        'project__id',
                                        'position__id',
                                        'status',
                                        'reverse_status'
                                        )

    return render(request, "accounts/applications.html", {
        'applicants': applicants,
        'my_positions': my_positions,
        'my_projects': my_projects,
        'statuses': statuses
    })


@login_required
def approve_applications(request, user_pk, application_pk, decision):
    """Approve or Reject Applicants"""

    # Get current Applicant Status
    reverse_status = Applicant.objects.get(pk=application_pk).status

    # If Applicant Status is new, change it rejected
    if reverse_status == "new":
        reverse_status = "rejected"

    # Change Applicant Status and reverse status to keep button functioning as appropriate
    Applicant.objects.filter(pk=application_pk).update(status=decision, reverse_status=reverse_status)

    # Send email to Applicant to alert them if they have been accepted or rejected
    send_email(Applicant.objects.get(pk=application_pk))

    return redirect('accounts:applications', pk=user_pk)


@login_required
def filter_applications(request, user_pk, filter):
    """Filter for all of the Applicants for my Project's Position(s)"""

    """PROJECT RELATED FILTERING"""
    # query all Project(s) that belong to current logged in User
    my_projects = Project.objects.filter(owner_id=user_pk).values()

    # build list of all Project id's belonging to current logged in User
    my_project_ids = [ids['id'] for ids in my_projects]

    # filter for all Project(s) that the current User is associated with
    my_filtered_projects = Project.objects.filter(Q(owner_id=user_pk) & Q(name__icontains=filter)).values()

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
    statuses = ["New", "Approved", "Rejected"]

    # query all Applicants associated with my Projects
    my_applications = Applicant.objects.filter(Q(project_id__in=my_project_ids) &
                                               Q(status__icontains=filter)
                                               ).values()

    # build list of all Applicant id's belonging to current logged in User w/ filters applied
    my_application_ids = [ids['id'] for ids in my_applications]

    """ASSEMBLE FINAL FILTER"""
    # query list of all Applicant(s) who have applied to current User's Project(s)
    queryset = Applicant.objects.filter(
        Q(project_id__in=my_filtered_project_ids) |
        Q(position_id__in=my_filtered_position_ids) |
        Q(id__in=my_application_ids)
    )

    # print(queryset)

    # join related Applicant and Position models to Applicant(s) who have applied to current User's Project(s)
    joined_queryset = queryset.select_related("applicant").select_related("position")

    # return values for Applicant, id, full name, position title, project name, and status to return to view
    applicants = joined_queryset.values('applicant_id',
                                        'id',
                                        'applicant__full_name',
                                        'position__title',
                                        'project__name',
                                        'project__id',
                                        'position__id',
                                        'status',
                                        'reverse_status'
                                        )

    print(applicants)

    return render(request, "accounts/applications.html", {
        'applicants': applicants,
        'my_positions': my_positions,
        'my_projects': my_projects,
        'statuses': statuses,
        'user_pk': user_pk,
    })
