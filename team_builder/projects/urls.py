from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.project_view, name="project"),
    url(r'^(?P<pk>\d+)/edit/$', views.EditProject, name="edit_project"),
    url(r'^new/$', views.NewProject, name="new_project"),
    url(r'^(?P<pk>\d+)/discard/$', views.DiscardProject.as_view(), name="discard_project"),
]
