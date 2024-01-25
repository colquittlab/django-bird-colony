# -*- coding: utf-8 -*-
# -*- mode: python -*-
from __future__ import unicode_literals

import uuid
import datetime
import posixpath as pp

import ipdb

from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import OuterRef, Subquery
from auditlog.registry import auditlog

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


@python_2_unicode_compatible
class Species(models.Model):
    common_name = models.CharField(max_length=45)
    genus = models.CharField(max_length=45)
    species = models.CharField(max_length=45)
    code = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.common_name

    class Meta:
        ordering = ['common_name']
        verbose_name_plural = 'species'
        unique_together = ("genus", "species")


@python_2_unicode_compatible
class Color(models.Model):
    name = models.CharField(max_length=12, unique=True)
    abbrv = models.CharField('Abbreviation', max_length=3, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


@python_2_unicode_compatible
class Status(models.Model):
    name = models.CharField(max_length=16, unique=True)
    count = models.SmallIntegerField(default=0, choices=((0, '0'), (-1, '-1'), (1, '+1')),
                                     help_text="1: animal acquired; -1: animal lost; 0: no change")
    category = models.CharField(max_length=2, choices=(('B','B'),('C','C'),('D','D'),('E','E')),
                                blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'status codes'

@python_2_unicode_compatible
class NestStatus(models.Model):
    name = models.CharField(max_length=16, unique=True)
    #count = models.SmallIntegerField(default=0, choices=((0, '0'), (-1, '-1'), (1, '+1')),
    #                                 help_text="1: animal acquired; -1: animal lost; 0: no change")
    #category = models.CharField(max_length=2, choices=(('B','B'),('C','C'),('D','D'),('E','E')),
    #                            blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'nest status codes'

@python_2_unicode_compatible
class Location(models.Model):
    name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Nest(Location):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    sire = models.ForeignKey('Animal',related_name="nest_sire", on_delete=models.SET_NULL, null=True)
    dam = models.ForeignKey('Animal', related_name="nest_dam", on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    nest_bands1 =  models.ForeignKey('Color',
                                    related_name='nest_band1',
                                    on_delete=models.SET_NULL,
                                    blank=True, null=True)
    nest_bands2 =  models.ForeignKey('Color',
                                    related_name='nest_band2',
                                    on_delete=models.SET_NULL,
                                    blank=True, null=True)

    def nest_bands(self):
        return '%s %s' % (self.nest_bands1.name, self.nest_bands2.name)

    #def __str__(self):
    #    return self.name

# class Breeder(models.Model):
#     animal = models.ForeignKey('Animal')
#     nest = models.ForeignKey('Nest')
#     established = models.DateTimeField(default = datetime.date.today)
#     removed = models.DateTimeField(default = datetime.date.today, blank=True,  null=True)


@python_2_unicode_compatible
class Age(models.Model):
    name = models.CharField(max_length=16,)
    min_days = models.PositiveIntegerField()
    max_days = models.PositiveIntegerField()
    species = models.ForeignKey('Species', on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s (%d-%d days)" % (self.species, self.name, self.min_days, self.max_days)

    class Meta:
        unique_together = ("name", "species")


class ThreshSum(models.Sum):
    """Returns True if Sum is greater than zero"""
    def convert_value(self, value, expresssion, connection, context):
        if value is None:
            return value
        return value > 0


class AnimalManager(models.Manager):
    def get_queryset(self):
        qs = super(AnimalManager, self).get_queryset()

        ## Subquery use described here: https://docs.djangoproject.com/en/2.0/ref/models/expressions
        newest = Event.objects.filter(animal=OuterRef('uuid')).order_by('-created')
        qs = qs.annotate(last_location=Subquery(newest.values('location__name')))

        return qs.annotate(alive=ThreshSum("event__status__count"))


class LivingAnimalManager(AnimalManager):
    def get_queryset(self):
        return super(LivingAnimalManager, self).get_queryset().filter(alive__exact=True)


class LastEventManager(models.Manager):
    """ Filters queryset so that only the most recent event is returned """
    def get_queryset(self):
        qs = super(LastEventManager, self).get_queryset()
        return qs.order_by("animal_id", "-date", "-created").distinct("animal_id")

class LastClaimManager(models.Manager):
    """ Filters queryset so that only the most recent claim is returned """
    def get_queryset(self):
        qs = super(LastClaimManager, self).get_queryset()
        return qs.order_by("-date")

#class LastLocationManager(models.Manager):
#    """ Filters queryset so that only the most recent location is returned """
#    def get_queryset(self):

@python_2_unicode_compatible
class Parent(models.Model):
    child = models.ForeignKey('Animal', related_name="+", on_delete=models.CASCADE)
    parent = models.ForeignKey('Animal', related_name="+", on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return "%s -> %s" % (self.parent, self.child)
    
@python_2_unicode_compatible    
class GeneticParent(models.Model):
    genchild = models.ForeignKey('Animal', related_name="+", on_delete=models.CASCADE)
    genparent = models.ForeignKey('Animal', related_name="+", on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return "%s -> %s" % (self.genparent, self.genchild)



@python_2_unicode_compatible
class Animal(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN_SEX = 'U'
    SEX_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
        (UNKNOWN_SEX, 'unknown')
    )

    BINARY_CHOICES = (
        ('Y', 'yes'),
        ('N', 'no')        
    )
    

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    species = models.ForeignKey('Species', on_delete=models.PROTECT)
    sex = models.CharField(max_length=2, choices=SEX_CHOICES)
    song_speed = models.FloatField(max_length=4,null=True, blank=True)
    call_speed = models.FloatField(max_length=4,null=True, blank=True)
    seqvar = models.CharField(max_length=2, choices=BINARY_CHOICES,null=True, blank=True)
    repeats = models.CharField(max_length=2, choices=BINARY_CHOICES,null=True, blank=True)
    hatch_date = models.DateField(default=None, blank=True, null=True)
    band_color = models.ForeignKey('Color',
                                   related_name='b1',
                                   on_delete=models.SET_NULL,
                                   blank=True, null=True)
    band_number = models.IntegerField(blank=True, null=True)

    band_color2 = models.ForeignKey('Color',
                                    related_name='b2',
                                    on_delete=models.SET_NULL,
                                    blank=True, null=True)
    band_number2 = models.IntegerField(blank=True, null=True)

    parents = models.ManyToManyField('Animal',
                                     related_name='children',
                                     through='Parent',
                                     through_fields=('child', 'parent'))

    location = models.ForeignKey('Location',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='locations')

    nest = models.ForeignKey('Nest',
                             on_delete=models.PROTECT,
                             null=True,
                             related_name='nests')

    reserved_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    blank=True, null=True,
                                    on_delete=models.SET(get_sentinel_user),
                                    help_text="mark a bird as reserved for a specific user")
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def short_uuid(self):
        return str(self.uuid).split('-')[0] 

    def band(self):
        #ipdb.set_trace()
        if self.band_number and not self.band_number2:
            if self.band_color:
                return "%s_%d" % (self.band_color, self.band_number)
            else:
                return "%d" % self.band_number
        elif self.band_number and self.band_number2:
            if self.band_color2:
                return "%s%d%s%d" % (self.band_color, self.band_number,
                                     self.band_color2, self.band_number2)
        else:
            return None

    def name(self):
        #
        return "%s_%s" % (self.species.code, self.band() or self.short_uuid())

    def __str__(self):
        return self.name()

    def sire(self):
        return self.parents.filter(sex__exact='M').first()

    def dam(self):
        return self.parents.filter(sex__exact='F').first()

    def nchildren(self):
        """ Returns (living, total) children """
        chicks = self.children
        return (chicks.filter(alive__exact=True).count(),
                chicks.count())

    objects = AnimalManager()
    living = LivingAnimalManager()

    def acquisition_event(self):
        """ Returns event when bird was acquired.

        Returns None if no acquisition events
        """
        return self.event_set.filter(status__count=1).order_by('date').first()

    def age_days(self):
        """ Returns days since birthdate if alive, age at death if dead, or None if unknown"""
        q_birth = self.event_set.filter(status__name="hatched").aggregate(d=models.Min("date"))
        if q_birth["d"] is None:
            return None
        if self.alive:
            return (datetime.date.today() - q_birth["d"]).days
        else:
            q_death = self.event_set.filter(status__count__lt=0).aggregate(d=models.Max("date"))
            return (q_death["d"] - q_birth["d"]).days

    # def last_location(self):
    #    """ Returns the location recorded in the most recent event """
    #    return self.event_set.order_by("-date", "-created").first().location

    def get_absolute_url(self):
        return reverse("birds:animal", kwargs={'uuid': self.uuid})

    class Meta:
        ordering = ['band_color', 'band_number']


@python_2_unicode_compatible
class Event(models.Model):
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    status = models.ForeignKey('Status', on_delete=models.PROTECT)
    location = models.ForeignKey('Location', blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)

    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET(get_sentinel_user))
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    latest = LastEventManager()

    def __str__(self):
        return "%s: %s on %s" % (self.animal, self.status, self.date)

    def event_date(self):
        """ Description of event and date """
        return "%s on %s" % (self.status, self.date)

    class Meta:
        ordering = ['-date']


@python_2_unicode_compatible
class NestEvent(models.Model):
    nest = models.ForeignKey('Nest', on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    status = models.ForeignKey('NestStatus', on_delete=models.PROTECT)
    number = models.SmallIntegerField(default=0)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET(get_sentinel_user))

    objects = models.Manager()
    latest = LastEventManager()

    def __str__(self):
        return "%s: %s on %s" % (self.nest, self.status, self.date)

    def event_date(self):
        """ Description of event and date """
        return "%s on %s" % (self.status, self.date)

    class Meta:
        ordering = ['-date']

class Claim(models.Model):
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True)

    latest = LastClaimManager()
    object = models.Manager()

auditlog.register(Nest)
