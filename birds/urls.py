# -*- coding: utf-8 -*-
# -*- mode: python -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url

from birds import views

urlpatterns = [
    # browser ui

    url(r'^$', views.IndexView.as_view(), name='index'),

    # Birds
    #url(r'^animals/$', views.AnimalList.as_view(), name='animals'),
    url(r'^animals/$', views.AnimalTableList.as_view(), name='animals'),
    url(r'^animals_search/$', views.AnimalSearch.as_view(), name='animals_search'),
    url(r'^animals_search_display/$', views.AnimalSearchDisplay.as_view(), name='animals_search_display'),
    url(r'^animals/new/$', login_required(views.BandingEntry.as_view()), name='new_animal'),
    url(r'^animals/(?P<uuid>[a-f0-9\-]{36})/$', views.AnimalView.as_view(), name='animal'),

    # Events
    url(r'^animals/(?P<animal>[a-f0-9\-]{36})/events/$',
        views.EventList.as_view(), name='animal_events'),
    url(r'^animals/(?P<uuid>[a-f0-9\-]{36})/events/new/$',
        login_required(views.EventEntry.as_view()), name='new_event'),
    url(r'^animals/(?P<uuid>[a-f0-9\-]{36})/events/new/$',
        login_required(views.NestEventEntry.as_view()), name='new_event'),    
    url(r'^events/$', views.EventList.as_view(), name='events'),
        url(r'^events/new/$', login_required(views.EventEntry.as_view()), name='new_event'),

    # Nests
    url(r'^nests/$', views.NestTableList.as_view(), name='nests'),
    url(r'^nests/(?P<uuid>[a-f0-9\-]{36})/$', views.NestView.as_view(), name='nest'),
    url(r'^nests/(?P<uuid>[a-f0-9\-]{36})/events/new/$', login_required(views.NestEventEntry.as_view()), name='nest_event'),
       url(r'^nests/events/new/$', login_required(views.NestEventEntry.as_view()), name='nest_event'),
 
    # Summary views
    url(r'^summary/events/([0-9]{4})/([0-9]{1,2})/$', views.EventSummary.as_view(),
        name="event_summary"),
    # forms
    url(r'^clutch$', login_required(views.ClutchEntry.as_view()), name='clutch'),
    # api
    url(r'^api/animals/$', views.APIAnimalsList.as_view(), name="animals_api"),
    url(r'^api/animals/(?P<pk>[a-f0-9\-]{36})/$', views.APIAnimalDetail.as_view()),
    #url(r'^api/animals/(?P<uuid>[a-f0-9\-]{36})/events$', views.APIEventsList.as_view()),
    url(r'^api/events/$', views.APIEventsList.as_view(), name="events_api"),
 
    ## LOGIN/LOGOUT
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'birds:login'}, name='logout')
]

urlpatterns += staticfiles_urlpatterns()
