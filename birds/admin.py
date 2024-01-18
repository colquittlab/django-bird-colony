
import datetime

from django.contrib import admin
from birds.models import Species, Color, Location, Animal, Event, Status, Age, Parent, Nest, NestEvent
from django.db import models



class ParentInline(admin.TabularInline):
    model = Parent
    fk_name = 'child'
    max_num = 2
    min_num = 2

class EventInline(admin.TabularInline):
    model = Event
    max_num = 1
    extra = 1

    def model_admin_callable(self, animal):
        return animal.event_set

class NestEventInline(admin.TabularInline):
    model = NestEvent
    max_num = 1
    extra = 1

    def model_admin_callable(self, animal):
        return animal.event_set

class AnimalInline(admin.TabularInline):
    model = Animal
    fk_name = 'nest'
    readonly_fields = ('uuid',)
    max_num = 1
    ordering = ('-hatch_date',)   
    fields = ('sex', 'nest', 'band_color', 'band_number', 'band_color2', 'band_number2', 'song_speed','call_speed', 'reserved_by', 'location')

class AnimalAdmin(admin.ModelAdmin):
 
    fields = ('sex', 'nest', 'band_color', 'band_number', 'band_color2', 'band_number2', 'song_speed','call_speed','seqvar','repeats', 'reserved_by')    
    list_display = ('name', 'band', 'age_days', 'species', 'nest', 'uuid', 'sex', 'song_speed','call_speed','seqvar','repeats', 'reserved_by')
    list_filter = ('sex', 'nest', 'band_color', 'reserved_by')
    search_fields = ('band_color__name', '=band_number', 'nest__name')
    inlines = (ParentInline,EventInline)

    def age_days(self, obj):
        return obj.age_days()
    age_days.admin_order_field = 'hatch_date'

    def band(self, obj):
        return obj.band()

    class Meta:
        ordering = ('age_days',)


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    fields = ('animal', 'status', 'location', 'description', 'date', 'entered_by')
    list_display = ('animal', 'date', 'status', 'description')
    list_filter = ('animal', 'entered_by', 'status', 'location')
    search_fields = ('description',)

class NestAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fields = ('name', 'sire', 'dam', 'nest_bands1', 'nest_bands2', 'uuid')
    list_display = ('name', 'sire', 'dam', 'nest_bands', 'created', 'uuid')
    list_display = ('name', 'sire', 'dam', 'created', 'uuid')
    search_fields = ('name', 'nest_bands',  'sire', 'dam')
    list_filter = ('name',)


    inlines = (AnimalInline,NestEventInline)

    def nest_bands(self, obj):
        return obj.nest_bands()

class NestEventAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    fields = ('date', 'nest', 'status', 'number', 'entered_by')
    list_display = ('date', 'nest', 'status', 'number', 'entered_by')
    list_filter =  ('nest', 'status', 'entered_by')
    search_fields = ('nest', 'status')

class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'count')

admin.site.register(Animal, AnimalAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Nest, NestAdmin)
admin.site.register(NestEvent, NestEventAdmin)
admin.site.register(Status, StatusAdmin)

for model in (Species, Color, Location, Age):
    admin.site.register(model)
