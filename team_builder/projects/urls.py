from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.view_project, name="project"),
    url(r'^(?P<pk>\d+)/edit/$', views.edit_project, name="edit_project"),
    url(r'^new/$', views.new_project, name="new_project"),
    url(r'^(?P<pk>\d+)/discard/$', views.DiscardProject.as_view(), name="discard_project"),
]
