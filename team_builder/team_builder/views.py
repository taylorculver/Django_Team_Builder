from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, render, redirect

from projects.models import Position, Project


def home(request):
    positions = Position.objects.values('title').distinct().order_by('title')
    projects = Project.objects.all()
    return render(request, 'index.html', {
        'positions': positions,
        'projects': projects
    })
