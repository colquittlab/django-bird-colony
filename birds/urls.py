# -*- coding: utf-8 -*-
# -*- mode: python -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import re_path

from birds import views

urlpatterns = [
    # browser ui

    re_path(r'^$', views.IndexView.as_view(), name='index'),

    # Birds
    #re_path(r'^animals/$', views.AnimalList.as_view(), name='animals'),
    re_path(r'^animals/$', views.AnimalTableList.as_view(), name='animals'),
    re_path(r'^animals_search/$', views.AnimalSearch.as_view(), name='animals_search'),
    re_path(r'^animals_search_display/$', views.AnimalSearchDisplay.as_view(), name='animals_search_display'),
    re_path(r'^animals/new/$', login_required(views.BandingEntry.as_view()), name='new_animal'),
    re_path(r'^animals/(?P<uuid>[a-f0-9\-]{36})/$', views.AnimalView.as_view(), name='animal'),

    # Events
    re_path(r'^animals/(?P<animal>[a-f0-9\-]{36})/events/$',
        views.EventList.as_view(), name='animal_events'),
    re_path(r'^animals/(?P<uuid>[a-f0-9\-]{36})/events/new/$',
        login_required(views.EventEntry.as_view()), name='new_event'),
    re_path(r'^animals/(?P<uuid>[a-f0-9\-]{36})/events/new/$',
        login_required(views.NestEventEntry.as_view()), name='new_event'),    
    re_path(r'^events/$', views.EventList.as_view(), name='events'),
        re_path(r'^events/new/$', login_required(views.EventEntry.as_view()), name='new_event'),

    # Nests
    re_path(r'^nests/$', views.NestTableList.as_view(), name='nests'),
    re_path(r'^nests/(?P<uuid>[a-f0-9\-]{36})/$', views.NestView.as_view(), name='nest'),
    re_path(r'^nests/(?P<uuid>[a-f0-9\-]{36})/events/new/$', login_required(views.NestEventEntry.as_view()), name='nest_event'),
       re_path(r'^nests/events/new/$', login_required(views.NestEventEntry.as_view()), name='nest_event'),

    # Eggs
    re_path(r'^eggs/$', views.EggTableList.as_view(), name='eggs'),
        re_path(r'^eggs/new/$', login_required(views.EggEntry.as_view()), name='new_eggs'),
    
    # Matings
    re_path(r'^matings/$', views.MatingTableList.as_view(), name='matings'),
        re_path(r'^matings/new/$', login_required(views.MatingEntry.as_view()), name='new_mating'),
    
    # Summary views
    re_path(r'^summary/events/([0-9]{4})/([0-9]{1,2})/$', views.EventSummary.as_view(),
        name="event_summary"),
    # forms
    re_path(r'^clutch$', login_required(views.ClutchEntry.as_view()), name='clutch'),
    # api
    re_path(r'^api/animals/$', views.APIAnimalsList.as_view(), name="animals_api"),
    re_path(r'^api/animals/(?P<pk>[a-f0-9\-]{36})/$', views.APIAnimalDetail.as_view()),
    #re_path(r'^api/animals/(?P<uuid>[a-f0-9\-]{36})/events$', views.APIEventsList.as_view()),
    re_path(r'^api/events/$', views.APIEventsList.as_view(), name="events_api"),
 
    ## LOGIN/LOGOUT
    re_path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': 'birds:login'}, name='logout')
]

urlpatterns += staticfiles_urlpatterns()
