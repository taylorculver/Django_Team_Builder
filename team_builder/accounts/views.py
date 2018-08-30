from django.contrib import messages
from django.contrib.auth import (authenticate, login,
                                 logout, update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm,
                                       UserCreationForm, PasswordChangeForm)
from django.core.urlresolvers import reverse
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView, TemplateView

from . import models
from . import forms
from .apps import Project, Position, Applicant


# @login_required(login_url='/accounts/sign_in/')
# def profile(request, pk):
#     user = get_object_or_404(models.User, id=pk)
#     project = Project.objects.filter(owner_id=pk)
#     return render(request, 'accounts/profile.html',
#                   {'user': user},
#                   {'project': project}
#                   )

# @login_required(login_url='/accounts/sign_in/')
class Profile(DetailView):
    """
    Show individual projects and associated positions

    Get Context Data for Second Model:
    https://docs.djangoproject.com/en/1.9/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_data

    """
    model = models.User
    template_name = "accounts/profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['user'] = models.User.objects.get(id=self.kwargs.get('pk'))
        context['projects'] = Project.objects.filter(owner_id=self.kwargs['pk'])
        context['skills'] = models.Skill.objects.filter(profile_id=models.Profile.objects.get(username_id=self.kwargs['pk']).id)
        return context


@login_required
def edit_profile(request, pk):
    user = models.User.objects.get(pk=pk)
    projects = Project.objects.filter(owner_id=pk)
    profile = models.Profile.objects.get(username_id=pk)

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


# def add_skills(request, pk):
#     profile = models.Profile.objects.get(pk=pk)
#     SkillsInLineFormset = inlineformset_factory(models.Profile, models.Skill, fields=('skill',), max_num=1, can_delete=False)
#     if request.method == "POST":
#         formset = SkillsInLineFormset(request.POST, request.FILES, instance=profile)
#         if formset.is_valid():
#             formset.save()
#             # Do something. Should generally end with a redirect. For example:
#             return HttpResponseRedirect(profile.get_absolute_url())
#     else:
#         formset = SkillsInLineFormset(instance=profile)
#     return render(request, 'accounts/formsetfactorytest.html', {'formset': formset})

def sign_in(request):
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
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


def applications_view(request, pk):
    applicants = Applicant.objects.all()
    # print(applicants)
    projects = Project.objects.all()
    positions = Position.objects.all()
    return render(request, "accounts/applications.html", {
        'pk': pk,
        'applicants': applicants,
        'projects': projects,
        'positions': positions
    })

# class Applications(TemplateView):
#     template_name = "accounts/applications.html"
