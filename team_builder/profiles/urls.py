from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.Profile.as_view(), name="profile"),
    url(r'^(?P<pk>\d+)/edit/$', views.EditProfile, name="edit_profile"),
]
