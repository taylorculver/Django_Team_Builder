from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, TemplateView

from . import models
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
        context['positions'] = Position.objects.filter(project_id=40) # Project.objects.filter(owner_id=self.kwargs['pk']).values_list('id')[0])
        return context








class EditProfile(TemplateView):
    template_name = "profiles/profile_edit.html"
