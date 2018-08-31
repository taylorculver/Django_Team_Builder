from django.db.models import Q
from django.shortcuts import render, redirect

from projects.models import Position, Project


def home(request):
    """Redirects User to respective Profile page"""
    user = request.user.id
    return redirect('accounts:profile', pk=user)


def all_projects(request):
    """Redirects User clean search & filter page"""
    positions = Position.objects.values('title').distinct().order_by('title')
    projects = Project.objects.all()
    return render(request, 'index.html', {
        'projects': projects,
        'positions': positions
    })



def search(request):
    """Searches database by Project title or description"""
    term = request.GET.get('q')
    positions = Position.objects.values('title').distinct().order_by('title')
    projects = Project.objects.filter(Q(name__icontains=term) | Q(description__icontains=term))
    return render(request, 'index.html', {
        'projects': projects,
        'positions': positions
    })


def filter(request, filter):
    """Filters database and returns all Projects for selected Positions"""
    # Query all Positions distinct title values
    positions = Position.objects.values('title').distinct().order_by('title')

    # Filter all queried Positions by selected Position title
    filtered_positions = Position.objects.filter(title__icontains=filter).distinct().order_by('title')

    # Filter for all distinct Project id's associated with filtered Positions
    project_ids = Position.objects.filter(title__icontains=filter).values('project_id').distinct()

    # Create list of all filtered Project id's
    project_ids_list = [ids['project_id'] for ids in project_ids]

    # Query all Projects related to Positions with a Project id in the above list
    projects = Project.objects.filter(id__in=project_ids_list)

    return render(request, 'index.html', {
        'positions': positions,
        'filtered_positions': filtered_positions,
        'projects': projects
    })
