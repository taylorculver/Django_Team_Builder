from django.conf.urls import url

from . import views

urlpatterns = [

    # view a single Project
    url(r'^(?P<pk>\d+)/$', views.view_project, name='project'),

    # Edit a single Project
    url(r'^(?P<pk>\d+)/edit/$', views.edit_project, name='edit_project'),

    # Create a single Project
    url(r'^new/$', views.new_project, name='new_project'),

    # Delete a single Project
    url(r'^(?P<pk>\d+)/discard/$', views.DiscardProject.as_view(),
        name='discard_project'),
]
