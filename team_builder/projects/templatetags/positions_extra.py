from django import template

from projects.models import Position

register = template.Library()

positions = Position.objects.values('title').distinct().order_by('title')
filters = [title['title'] for title in positions]


@register.inclusion_tag('positions_nav.html')
def nav_positions_list():
    return {'filters': filters}
