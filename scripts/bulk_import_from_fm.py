#! /usr/bin/env python

"""
Load FileMaker bird records in csv format to django-bird-colony sqlite3 db
"""

import sys
#import sqlite3
#import argparse
import ipdb

import django.db
from birds.models import Animal, Event, Status, Location, Color, Species, Parent, Nest

class Parser:


    function_dict = {'Animal': process_Animal,
                     'Nest' : process_Nest,
                     'NestEvent': process_NestEvent,
                     'Location' : process_Location
    }

    """
    birdID
    hatch_early
    hatch_late
    used,
    Nest
    Location
    Claimed_by
    Father
    Mother
    CurrentAge

    Sex
    Notes
    SongsLocation
    ClaimedDate
    SpectrogramFilename
    MoveHistory
    ClaimHistory
    ID_unique
    Alive
    Deathdate
    GeneticSource
    GeneticSource_confirmation
    NA,NA,NA,NA
    """
    index_Animal = {'band' : 0,
                    'hatch_date' : 1,
                    'nest' : 4,
                    'location':5,
                    'reserved_by':6,
                    'sire' : 7,
                    'dam' : 8,
                    'sex' : 10,
                    'notes' : 11,
                    'reserved_date' : 13,
                    'death_date' : 19
    }

    """
    nest
    dam
    sire
    notes
    nest_bands
    songs_loc
    parentage
    colonychecks_notes
    eggs
    hatchlings
    fledglings
    notes_history
    egg_date
    hatch_date
    global_90date
    """

    index_Nest = {'nest' : 0,
                  'dam' : 1,
                  'sire': 2,
                  'notes': 3,
                  'nest_bands' : 4}

    """
    date,nest,number,event,user
    """
    index_NestEvent = {'date' : 0,
                       'nest' : 1,
                       'number' : 2,
                       'event' : 3,
                       'uesr' : 4}

    index_Location = {}
    record_index = {'Animal': index_Animal,
                    'Nest' : index_Nest,
                    'NestEvent' : index_NestEvent,
                    'Location' : index_Location}

    def __init__(self, ifname):
        self.ifname = ifname
        self.ifile = open(self.ifname)

    def process(self, method):

        for record in self.ifile:
            ipdb.set_trace()
            record_s = record.strip.split(",")
            record_dict = {}
            for key, val in record_index[method].items():
                record_dict[key] = record_s[val]
            try:
                function_dict[method](record_dict)
            except django.db.Error as e:
                print(e.__cause__)

    def process_Animal(self, record_dict):
        bird = Animal(species = "BF",
                       sex = record_dict['sex'],
                       band = record_dict['band'],
                       nest = record_dict['nest'],
                       reserved_by = record_dict['reserved_by'],
                       created = record_dict['created']
                       )

        if record_dict['sire'] and record_dict['dam']:
            Parent.objects.create(child=bird, parent=data['sire'])
            Parent.objects.create(child=bird, parent=data['dam'])

        bird.save()

        evt = Event(animal=bird,
                    date=record_dict['hatch_date'],
                    status='hatched',
                    description=None,
                    location=data['nest'],
                    entered_by=record_dict['entered_by'])
        evt.save()

        evt = Event(animal=bird,
                    date=data['banding_date'],
                    status=data['band_status'],
                    location=data['location'],
                    description=bird.band,
                    entered_by=data['entered_by'])
        evt.save()

    def process_Nest(self, record_dict):
        nest = Nest(name = record_dict['name'],
                    sire = record_dict['sire'],
                    dam = record_dict['dam'],
                    created = record_dict['date_created'])
        nest.save()
        pass

    def process_NestEvent(self, record_dict):
        evt = NestEvent(nest = record_dict['nest'],
                        date = record_dict['date'],
                        status = record_dict['status'],
                        number = record_dict['number'],
                        entered_by = record_dict['entered_by'])
        evt.save()

    def process_Location(self, record_s):
        pass




bird_file = "fm_data/birds_clean.csv"
nest_file = "fm_data/nests_clean.csv"
nestevent_file = "fm_data/eggs_clean.csv"

p = Parser(bird_file)
p.process('Animal')
