from django.contrib import messages
from django.contrib.auth import (authenticate, login,
                                 logout, update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm,
                                       UserCreationForm, PasswordChangeForm)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView, TemplateView

from . import models
from . import forms
from .apps import Project, Position


@login_required(login_url='/accounts/sign_in/')
def profile(request, username):
    user = get_object_or_404(models.User, username=username)
    return render(request, 'accounts/profile.html', {'user': user})

# class Profile(DetailView):
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
#     queryset = models.User.objects.all()
#     template_name = "accounts/profile.html"
#     context_object_name = "profile"
#
#     def get_context_data(self, **kwargs):
#         context = super(Profile, self).get_context_data(**kwargs)
#         context['profile'] = models.Profile.objects.filter(id=self.kwargs['pk'])
#         context['projects'] = Project.objects.filter(owner_id=self.kwargs['pk'])
#         # context['positions'] = Position.objects.filter(project_id__in=Project.objects.filter(owner_id=self.kwargs['pk']).values_list('id'))
#         return context

@login_required
def edit_profile(request, username):
    user = get_object_or_404(models.User, username=username)
    # user_form = forms.UserForm(instance=user)
    profile_form = forms.ProfileForm(instance=user.profile)

    if request.method == 'POST':
        # user_form = forms.UserForm(instance=user, data=request.POST)
        profile_form = forms.ProfileForm(instance=user.profile,
                                         data=request.POST,
                                         files=request.FILES)
        if profile_form.is_valid():
            # user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(user.get_absolute_url())
    return render(request, 'accounts/profile_edit.html', {
        # 'user_form': user_form,
        'profile_form': profile_form
    })


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
                        reverse('accounts:profile', args=[user.username])
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
                'accounts:profile', args=[user.username]))
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))
