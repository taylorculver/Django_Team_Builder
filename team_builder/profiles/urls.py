from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'profile/$', views.Profile.as_view(), name="profile"),
    url(r'profile/edit/$', views.EditProfile.as_view(), name="edit_profile"),
]
