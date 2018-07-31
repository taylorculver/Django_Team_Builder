from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'project/$', views.Project.as_view(), name="project"),
    url(r'profile/new/$', views.NewProject.as_view(), name="new_project"),
    url(r'profile/edit/$', views.EditProject.as_view(), name="edit_project"),
]
