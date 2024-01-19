# -*- coding: utf-8 -*-
# -*- mode: python -*-
import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin
from django.db.models import Min, F
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from django_filters import rest_framework as filters_rest
import django_filters as filters
from django_filters.views import FilterView
from django_tables2 import RequestConfig
from django_tables2 import SingleTableMixin, SingleTableView
from birds.models import Animal, Event, Nest
from birds.serializers import AnimalSerializer, AnimalDetailSerializer, EventSerializer
from birds.forms import ClutchForm, BandingForm, EventForm, AnimalSearchForm, AnimalForm, NestEventForm 

from .tables import AnimalTable, NestTable

import ipdb

class AnimalFilter(filters.FilterSet):
    uuid = filters.CharFilter(field_name="uuid", lookup_expr="istartswith")
    color1 = filters.CharFilter(field_name="band_color", lookup_expr="exact")
    color2 = filters.CharFilter(field_name="band_color2", lookup_expr="exact")
    band1 = filters.NumberFilter(field_name="band_number", lookup_expr="exact")
    band2 = filters.NumberFilter(field_name="band_number2", lookup_expr="exact")
    location = filters.CharFilter(field_name="last_location", lookup_expr="exact")
    colorband = filters.CharFilter(field_name="band", lookup_expr="iexact")
    species = filters.CharFilter(field_name="species__code", lookup_expr="iexact")
    sex = filters.CharFilter(field_name="sex", lookup_expr="exact")
    repeats = filters.CharFilter(field_name="repeats", lookup_expr="exact")
    seqvar = filters.CharFilter(field_name="seqvar", lookup_expr="exact")
    
    nest = filters.CharFilter(field_name="nest__uuid", lookup_expr="exact")
    available = filters.BooleanFilter(field_name="reserved_by", lookup_expr="isnull")
    reserved_by = filters.CharFilter(field_name="reserved_by__username", lookup_expr="iexact")
    reserved_by_name = filters.CharFilter(field_name="reserved_by__username", lookup_expr="iexact")
    song_speed_greaterthan = filters.NumberFilter(field_name="song_speed", lookup_expr="gte");
    song_speed_lessthanthan = filters.NumberFilter(field_name="song_speed", lookup_expr="lte");
    call_speed_greaterthan = filters.NumberFilter(field_name="call_speed", lookup_expr="gte");
    call_speed_lessthanthan = filters.NumberFilter(field_name="call_speed", lookup_expr="lte");    
    parent = filters.CharFilter(field_name="parents__uuid", lookup_expr="istartswith")
    child = filters.CharFilter(field_name="children__uuid", lookup_expr="istartswith")
    alive = filters.BooleanFilter(field_name="alive", lookup_expr="exact", widget=filters.widgets.BooleanWidget() )

    class Meta:
        model = Animal
        fields = []


class EventFilter(filters.FilterSet):
    animal = filters.CharFilter(field_name="animal__uuid", lookup_expr="istartswith")
    color = filters.CharFilter(field_name="animal__band_color__name", lookup_expr="iexact")
    band = filters.NumberFilter(field_name="animal__band_number", lookup_expr="exact")
    species = filters.CharFilter(field_name="animal__species__code", lookup_expr="iexact")
    location = filters.CharFilter(field_name="location__name", lookup_expr="icontains")
    entered_by = filters.CharFilter(field_name="entered_by__username", lookup_expr="icontains")
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")

    class Meta:
        model = Event
        fields = {
            'date': ['exact', 'year', 'range'],
        }

class NestFilter(filters.FilterSet):
    uuid = filters.CharFilter(field_name="uuid", lookup_expr="istartswith")
    name = filters.CharFilter(field_name="name", lookup_expr="istartswith")
    sire = filters.CharFilter(field_name="sire__uuid", lookup_expr="istartswith")
    dam = filters.CharFilter(field_name="dam__uuid", lookup_expr="istartswith")

    class Meta:
        model = Nest
        fields = []

class AnimalList(FilterView):
    model = Animal
    filterset_class = AnimalFilter
    template_name = "birds/animal_list.html"

    def get_queryset(self):
        #order_by = request.GET.get('order_by', 'defaultOrderField')
        #self.model.objects.all().order_by('-age')

        if self.request.GET.get("living", False):
            qs = self.model.living.annotate(acq_date=Min("event__date"))#.order_by("acq_date")
        else:
            qs = self.model.objects.all()
        qs = qs.order_by('age')
        return qs


class AnimalTableList(SingleTableMixin, FilterView):
    model = Animal
    filterset_class = AnimalFilter
    table_class = AnimalTable
    template_name = "birds/animal_list2.html"

    def get_table_data(self):
        #self.model.objects.all().order_by('age')

        if self.request.GET.get("living", False):
            qs = self.model.living.annotate(acq_date=Min("event__date"))#.order_by("acq_date")
        else:
        #qs = self.model.objects.annotate(age_days=F("age_days")).order_by("age_days")
            qs = self.model.objects.all()
        qsf = AnimalFilter(self.request.GET, queryset=qs).qs
        #qsf = qsf.order_by('-age_days')
        return qsf

class EventList(FilterView, generic.list.MultipleObjectMixin):
    model = Event
    filterset_class = EventFilter
    template_name = "birds/event_list.html"
    paginate_by = 25

    def get_queryset(self):
        qs = Event.objects.filter(**self.kwargs)
        qs = qs.order_by("-date", "created")
        return qs

class NestTableList(SingleTableMixin, FilterView):
    model = Nest
    filterset_class = NestFilter
    table_class = NestTable
    template_name = "birds/nest_list.html"

    def get_table_data(self):
        qs = self.model.objects.all()
        qsf = NestFilter(self.request.GET, queryset=qs).qs
        return qsf

class AnimalView(generic.UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'birds/animal2.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


    def get_initial(self):
        initial = super(AnimalView, self).get_initial()

        ## Set reserved_by initial to current claimant
        current_bird = self.get_object()
        initial['reserved_by'] = current_bird.reserved_by
        return initial

    def children(self):
        return self.object.children.all()

    def event_list(self):
        events = self.object.event_set.all().order_by("-date", "-created")
        return events

    def claim_list(self):
        claims = self.object.claim_set.all().order_by("-date")
        return claims

    def form_valid(self, form, **kwargs):
        claims = form.update_claims(self.get_object())
        #uuids = [a.uuid for a in objs['chicks']]
        #qs = self.model.objects.filter(uuid__in = uuids)
        #table = ClaimTable(qs)
        return super().form_valid(form)
        # return render(self.request, 'birds/animal2.html',
        #               {'form' : form})


class NestView(generic.DetailView):
    model = Nest
    template_name = 'birds/nest.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super(NestView, self).get_context_data(**kwargs)
        animal = context['nest']
        #context['nest_list'] = animal.children.all()
        #context['nest_list'] = animal.event_set.all()
        return context

    def children(self):
        return Animal.filter(nest__name=self.object.name)

    def event_list(self):
        events = self.object.nestevent_set.all().order_by("-date")
        return events


class ClutchEntry(SingleTableMixin, generic.FormView):
    template_name = "birds/clutch_entry.html"
    form_class = ClutchForm
    model = Animal
    table_class = AnimalTable
    context_table_name = 'results'

    def get_initial(self):
        initial = super(ClutchEntry, self).get_initial()
        initial["user"] = self.request.user
        initial["results"] = None

        return initial

    def form_valid(self, form, **kwargs):
        """ For valid entries, render a page with a list clutch """
        objs = form.create_clutch()
        uuids = [a.uuid for a in objs['chicks']]
        qs = self.model.objects.filter(uuid__in = uuids)
        table = AnimalTable(qs)
        return render(self.request, 'birds/clutch_entry.html',
                      {'form' : form,
                       'results' : table})

    def get_table_data(self):
        qs = self.model.objects.all()
        post = self.request.POST
        qsf = AnimalFilter(post, queryset=qs).qs
        return qsf

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClutchEntry, self).get_context_data(**kwargs)

        if len(self.request.POST) == 0:
            table = None
        else:
            table = self.get_table(**self.get_table_kwargs())

        context[self.get_context_table_name(table)] = table
        return context


class BandingEntry(generic.FormView):
    template_name = "birds/banding_entry.html"
    form_class = BandingForm

    def get_initial(self):
        initial = super(BandingEntry, self).get_initial()
        initial["user"] = self.request.user
        return initial

    def form_valid(self, form, **kwargs):
        chick = form.create_chick()
        return HttpResponseRedirect(reverse('birds:animal', args=(chick.pk,)))

class NestEventEntry(generic.FormView):
    template_name = "birds/nest_event_entry.html"
    form_class = NestEventForm
   
    def get_initial(self):
     #   ipdb.set_trace() 
        initial = super(NestEventEntry, self).get_initial()
        
        try:        
            uuid = self.kwargs["uuid"]    
            initial['nest'] = uuid    
        except:
            pass
        initial['entered_by'] = self.request.user
        return initial

    def form_valid(self, form, **kwargs):
     #   ipdb.set_trace()
        event = form.save()
    #   return super().form_valid(form)
        return HttpResponseRedirect(reverse('birds:nest_event', args=(event.nest.pk,)))

  #  def form_invalid(self, form, **kwargs):    
    #    ipdb.set_trace()

class EventEntry(generic.FormView):
    template_name = "birds/event_entry.html"
    form_class = EventForm
 
    def get_initial(self):
        initial = super(EventEntry, self).get_initial()
        #ipdb.set_trace()
        try:
            
         uuid = self.kwargs["uuid"]
         animal = Animal.objects.get(uuid=uuid)
         initial['animal'] = animal
         initial['uuid'] = uuid
        except:
            pass
        initial['entered_by'] = self.request.user
        return initial

    def form_valid(self, form, **kwargs):        
        event = form.save()
      #  return super().form_valid(form)       
        return HttpResponseRedirect(reverse('birds:new_event', args=(event.animal.pk,)))

class AnimalSearchDisplay(SingleTableMixin, generic.FormView):
    template_name = "birds/animals_search_display.html"
    model = Animal
    form_class = AnimalSearchForm
    table_class = AnimalTable
    context_table_name = 'results'

    def get_initial(self):
        initial = super(AnimalSearchDisplay, self).get_initial()
        initial["user"] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
       # Call the base implementation first to get a context
       context = super(AnimalSearchDisplay, self).get_context_data(**kwargs)
       return context

    def form_valid(self, form, **kwargs):
        animal_qs = Animal.objects.all()
        animal_filter = AnimalFilter(self.request.GET, queryset=animal_qs).qs
        table = self.get_table()
        return render(self.request, 'birds/animals_search.html', {'results' : table,
                                                                  'form': form})
    def get_table_data(self):
        order_by = self.request.GET.get('sort')

        if self.request.GET.get("living", False):
            qs = self.model.living.annotate(acq_date=Min("event__date")).order_by("acq_date")
        else:
            qs = self.model.objects.all()

        qsf = AnimalFilter(self.request.GET, queryset=qs).qs
        if order_by:
            qsf = qsf.order_by(order_by)
        else:
            qsf = qsf.order_by('-age_days')
        return qsf

class AnimalSearch(SingleTableMixin, generic.FormView):
    template_name = "birds/animals_search.html"
    model = Animal
    form_class = AnimalSearchForm
    table_class = AnimalTable
    context_table_name = 'results'

    def get_initial(self):
        initial = super(AnimalSearch, self).get_initial()
        initial["user"] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
       # Call the base implementation first to get a context
       context = super(AnimalSearch, self).get_context_data(**kwargs)
       return context

    def form_valid(self, form, **kwargs):
        animal_qs = Animal.objects.all()
        animal_filter = AnimalFilter(self.request.GET, queryset=animal_qs).qs
        table = self.get_table()
        return render(self.request, 'birds/animals_search.html', {'results' : table,
                                                                  'form': form})
    def get_table_data(self):
        order_by = self.request.GET.get('sort')

        if self.request.GET.get("living", False):
            qs = self.model.living.annotate(acq_date=Min("event__date")).order_by("acq_date")
        else:
            qs = self.model.objects.all()

        qsf = AnimalFilter(self.request.GET, queryset=qs).qs
        if order_by:
            qsf = qsf.order_by(order_by)
        else:
            qsf = qsf.order_by('-age_days')
        return qsf

class IndexView(generic.base.TemplateView):
    template_name = "birds/index.html"

    def get_context_data(self, **kwargs):
        today = datetime.date.today()
        return {"today": today,
                "lastmonth": today.replace(day=1) - datetime.timedelta(days=1)
        }


class EventSummary(generic.base.TemplateView):
    template_name = "birds/summary.html"

    def get_context_data(self, **kwargs):
        from collections import Counter
        tots = Counter()

      #  if len(self.args)>=2:
        year, month = map(int, self.args[:2])
        if month!=13:
            for event in Event.objects.filter(date__year=year, date__month=month):
                tots[event.status.name] += 1
            return { "year": year,
                     "month": month,
                     "next": datetime.date(year, month, 1) + datetime.timedelta(days=32),
                     "prev": datetime.date(year, month, 1) - datetime.timedelta(days=1),
                     "event_totals": dict(tots) }
        else:
          fullyear=[year,year,year,year,year,year,year,year,year,year,year,year]
          fullyear[0]=year-1;
          fullyear[1]=year-1;
          fullyear[2]=year-1;
          months=[9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]
          for i in range(12):
              
            for event in Event.objects.filter(date__year=fullyear[i], date__month=months[i]):
                tots[event.status.name] += 1
            #ipdb.set_trace()    
            return { "year": year,                                                           
                     "next": datetime.date(year+1, 12, 1) + datetime.timedelta(days=32),
                     "prev": datetime.date(year-1, 12, 1) - datetime.timedelta(days=1),
                 "event_totals": dict(tots) }

##class YearSummary(generic.base.TemplateView):
##    template_name = "birds/summary.html"
##
##    def get_context_data(self, **kwargs):
##        from collections import Counter
##        tots = Counter()
##
##        year, month = map(int, self.args[:2])
##            
##        # aggregation by month does not appear to work properly with postgres
##        # backend. Event counts per month will be relatively small, so this
##        # shouldn't be too slow
##        ipdb.set_trace();
##        fullyear=[year]^12
##        fullyear[0]=year-3;
##        fullyear[1]=year-3;
##        fullyear[2]=year-3;
##        months=[9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]
##        
##        for i in range(12):                
##            for event in Event.objects.filter(date__year=year[i], date__month=month[i]):
##                tots[event.status.name] += 1
##        return { "year": year,
##                "month": month,
##            #    "next": datetime.date(year, month, 1) + 365
##             #   "prev": datetime.date(year, month, 1) - 365
##                "event_totals": dict(tots) }

### API

class APIAnimalsList(generics.ListAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    filter_backends = (filters_rest.DjangoFilterBackend,)
    filter_class = AnimalFilter

    def get_queryset(self):
        if self.request.GET.get("living", False):
            qs = Animal.living.annotate(acq_date=Min("event__date")).order_by("acq_date")
        else:
            qs = Animal.objects.all()
        return qs


class APIAnimalDetail(generics.RetrieveAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalDetailSerializer


class APIEventsList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters_rest.DjangoFilterBackend,)
    filter_class = EventFilter


# Create your views here.
