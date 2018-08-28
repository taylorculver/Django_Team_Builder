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


# def search(request):
#     """Searches database by mineral name for entered free text term"""
#     term = request.GET.get('q')
#     minerals = models.Mineral.objects.filter(name__icontains=term)
#     return render(request, 'index.html', {'minerals': minerals})


def filter(request, filter):
    """filters database and returns all Projects for selected Positions"""
    positions = Position.objects.filter(filter=filter)
    print(positions)
    return render(request, 'index.html', {'positions': positions})
