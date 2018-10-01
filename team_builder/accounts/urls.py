from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sign_in/$', views.sign_in, name='sign_in'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^sign_out/$', views.sign_out, name='sign_out'),

    # To view a User's Profile
    url(r'^(?P<pk>\w+)/$', views.view_profile, name='profile'),

    # To edit a User's Profile
    url(r'^(?P<pk>\w+)/edit/$', views.edit_profile, name='edit_profile'),

    # To view all Applications
    url(r'^(?P<pk>\w+)/applications/$',
        views.view_applications,
        name='applications'),

    # To filter Applications by Project, Position, etc...
    url(r'^(?P<user_pk>\w+)/applications/filter/(?P<filter>.+?)/$',
        views.filter_applications,
        name='filter_applications'),

    # To change the status of an Applicant
    url(r'^(?P<user_pk>\w+)/applications/change-status/'
        r'(?P<application_pk>\w+)/(?P<decision>approved|rejected|new)/$',
        views.approve_applications,
        name='approve_applications'),

]
