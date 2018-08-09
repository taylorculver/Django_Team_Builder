from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView, TemplateView

from . import models
from . import forms
from .apps import Project, Position

# def Profile(request, pk):
#     user = get_object_or_404(models.User, id=pk)
#     return render(request, 'profiles/profile.html', {'user': user})


class Profile(DetailView):
    """
    Show individual projects and associated positions

    Get Context Data for Second Model:
    https://docs.djangoproject.com/en/1.9/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_data

    Obtain Postions Associated with Project Primary Key:
    https://stackoverflow.com/questions/25881015/django-queryset-return-single-value

    """
    queryset = models.User.objects.all()
    template_name = "profiles/profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['profile'] = models.Profile.objects.filter(id=self.kwargs['pk'])
        context['projects'] = Project.objects.filter(owner_id=self.kwargs['pk'])
        # context['positions'] = Position.objects.filter(project_id__in=Project.objects.filter(owner_id=self.kwargs['pk']).values_list('id'))
        return context


# @login_required
def EditProfile(request, pk):
    user = get_object_or_404(models.User, id=pk)
    print(pk)
    print(user.id)
    profile = models.Profile.objects.create(user=request.user)
    profile_form = forms.ProfileForm(instance=user.profile)
    print(profile_form)

    if request.method == 'POST':
        profile_form = forms.ProfileForm(instance=user.profile,
                                         data=request.POST,
                                         files=request.FILES)
        # print(profile_form)

        if profile_form.is_valid():

            profile_form.save()
            return redirect('profiles:profile', pk=pk)
    return render(request, 'profiles/profile_edit.html', {
        'profile_form': profile_form
    })
