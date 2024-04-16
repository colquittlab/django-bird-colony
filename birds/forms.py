# -*- coding: utf-8 -*-
# -*- mode: python -*-

import datetime
from django import forms

from django.contrib.auth.models import User
from birds.models import Animal, Event, Status, Location, Color, Species, GeneticParent, Parent, Nest, Mating, Claim, NestEvent, Egg, EggEvent, EggEventCode, ParentEgg

import ipdb

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ["animal", "date", "status", "location", "description", "entered_by"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        if len(self.initial.values())==3:
            self.fields['animal'] = forms.ModelChoiceField(queryset=(Animal.objects.filter(uuid__exact=self.initial.get('uuid'))))
        else:
            pass

    def create_event(self):
#        ipdb.set_trace()
        data = self.data
        if Status.objects.get(id=data['status']).name == 'moved':
            Animal.objects.filter(uuid=data['animal']).update(location=data['location'])


        #ipdb.set_trace()
        evt = Event(animal=Animal.objects.get(uuid=data['animal']),
                    date=data['date'],
                    status=Status.objects.get(id=data['status']),
                    description=data['description'],
                    location=Location.objects.get(id=data['location']),
                    entered_by=User.objects.get(id=data['entered_by']))
        evt.save()
        return(evt)
    
class NestEventForm(forms.ModelForm):   
    class Meta:
        model = NestEvent 
        fields = ["nest", "date", "event", "number",  "entered_by"]
        

    def __init__(self, *args, **kwargs):
        super(NestEventForm, self).__init__(*args, **kwargs)

class EggEventForm(forms.ModelForm):

    class Meta:
        model = EggEvent
        fields = ["egg", "date", "event", "location", "description", "entered_by"]

    def __init__(self, *args, **kwargs):
        super(EggEventForm, self).__init__(*args, **kwargs)
        #ipdb.set_trace()
        if len(self.initial.values())==4:
            
            egg_qs = Egg.objects.filter(uuid=self.initial.get('uuid'))
            egg_obj = egg_qs[0]
            self.fields['egg'] = forms.ModelChoiceField(queryset=egg_qs)
            
            current_location = egg_obj.location
            if current_location is None:
                current_location = egg_obj.nest
            self.fields['location'] = forms.ModelChoiceField(queryset = Location.objects.filter(name=self.initial.get('location')))
        else:
            pass

    def create_event(self):
#        ipdb.set_trace()
        data = self.data
        if Status.objects.get(id=data['event']).name == 'moved':
            Egg.objects.filter(uuid=data['egg']).update(location=data['location'])


        #ipdb.set_trace()
        evt = EggEvent(egg=Egg.objects.get(uuid=data['egg']),
                    date=data['date'],
                    event=EggEventCode.objects.get(id=data['event']),
                    description=data['description'],
                    location=Location.objects.get(id=data['location']),
                    entered_by=User.objects.get(id=data['entered_by']))
        evt.save()
        return(evt)
    
class BandingForm(forms.Form):
    acq_status = forms.ModelChoiceField(queryset=Status.objects.filter(count=1),
                                        initial=Status.objects.get(name__contains='hatched').id)
    acq_date = forms.DateField()
    sex = forms.ChoiceField(choices=(('M', 'male'),
                                     ('F', 'female'),
                                     ('U', 'unknown')))    
    seqvar = forms.ChoiceField(choices=(('yes','Y'),('no','N')),required=False)   
    repeats = forms.ChoiceField(choices=(('yes','Y'),('no','N')),required=False)
    nest = forms.ModelChoiceField(queryset=Nest.objects.all(), required=False)
    sire = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='M'),
                                  required=False)
    dam  = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='F'),
                                  required=False)
    geneticsire = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='M'),
                                  required=False)
    geneticdam  = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='F'),
                                  required=False)      
    species = forms.ModelChoiceField(queryset=Species.objects.all(), required=False,
                                     initial=Species.objects.get(code__exact='BF').id)
    banding_date = forms.DateField()
    band_color1 = forms.ModelChoiceField(queryset=Color.objects.all(), required=False)
    band_number1 = forms.IntegerField(min_value=1)
    band_color2 = forms.ModelChoiceField(queryset=Color.objects.all(), required=False)
    band_number2 = forms.IntegerField(min_value=1, required=False)
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    comments = forms.CharField(widget=forms.Textarea, required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all())

    def clean(self):
        super(BandingForm, self).clean()
        data = self.cleaned_data
        try:
            data['band_status'] = Status.objects.get(name__startswith="band")
        except:
            raise forms.ValidationError("No 'banded' status type - add one in admin")
        if 'acq_status' in data and data['acq_status'].name == "hatched":
            if (data['dam'] is None or data['sire'] is None) and data['nest'] is None:
                raise forms.ValidationError("Parents or Nest required for hatched birds")
            #if data['dam'].species != data['sire'].species:
            #    raise forms.ValidationError("Parents must be the same species")
            #data['species'] = data['dam'].species
        else:
            if data['species'] is None:
                raise forms.ValidationError("Species required for non-hatch acquisition")
            data['dam'] = None
            data['sire'] = None
        return data

    def create_chick(self):
        #ipdb.set_trace()
        data = self.cleaned_data
        band_list = map(lambda x : str(x), [data['band_color1'], data['band_number1'], data['band_color2'], data['band_number2']])
        band = band="".join(band_list)

        if data['acq_status'].name == 'hatched':
            hd = data['acq_date']
            if data['nest'] and not (data['sire'] or data['dam']):
                #ipdb.set_trace()
                nest_obj = Nest.objects.filter(name=data['nest'])[0]
                sire = nest_obj.current_mating().sire
                dam = nest_obj.current_mating().dam
            else:
                sire = data['sire']
                dam = data['dam']
        else:
            hd = None

        chick = Animal(species=data['species'], sex=data['sex'],
                       hatch_date=hd,
                       location=data['location'],
                       band_color=data['band_color1'], band_number=data['band_number1'],
                       band_color2=data['band_color2'], band_number2=data['band_number2'],   
                       nest=data['nest'])
        chick.save()
        chick.update_age_days()
        #birds.cron.update_age_days(chick)
        
        if data['acq_status'].name == 'hatched':
            Parent.objects.create(child=chick, parent=sire)
            Parent.objects.create(child=chick, parent=dam)
    
                    
        evt = Event(animal=chick, date=data['acq_date'],
                    status=data['acq_status'],
                    description=data['comments'],
                    location=data['location'],
                    entered_by=data['user'])
        evt.save()
        
        evt = Event(animal=chick, date=data['banding_date'],
                    status=data['band_status'],
                    location=data['location'],
                    description=chick.band,
                    entered_by=data['user'])
        evt.save()
        return chick


class ClutchForm(forms.Form):
    sire = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='M'), required=False)
    dam  = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='F'), required=False)
    geneticsire = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='M'), required=False)
    geneticdam  = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='F'), required=False)      
    nest = forms.ModelChoiceField(queryset=Nest.objects.all())
    chicks = forms.IntegerField(min_value=1)
    hatch_date = forms.DateField(initial=datetime.date.today)
    comments = forms.CharField(widget=forms.Textarea, required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all())

    def clean(self):
        super(ClutchForm, self).clean()
        try:
            self.cleaned_data['status'] = Status.objects.get(name__startswith="hatch")
        except:
            raise forms.ValidationError("No 'hatch' status type - add one in admin")

        #if ('dam' in self.cleaned_data and 'sire' in self.cleaned_data and
        #    self.cleaned_data['dam'].species != self.cleaned_data['sire'].species):
        #    raise forms.ValidationError("Parents must be the same species")
        return self.cleaned_data


    def create_clutch(self):
        ret = {'chicks': [], 'events': []}
        
        for i in range(self.cleaned_data['chicks']):

            if self.cleaned_data['nest'] is not None:
                nest_obj = Nest.objects.filter(name=self.cleaned_data['nest'])[0]
                sire = nest_obj.current_mating().sire
                dam = nest_obj.current_mating().dam
    
                geneticsire = sire
                geneticdam = dam

            if self.cleaned_data['geneticsire'] is not None:
                geneticsire = self.cleaned_data['geneticsire']
                
            if self.cleaned_data['geneticdam'] is not None:
                geneticdam = self.cleaned_data['geneticdam']
                
                
            if self.cleaned_data['sire'] is not None:
                sire = self.cleaned_data['sire']

            if self.cleaned_data['dam'] is not None:
                sire = self.cleaned_data['dam']

            if sire is None:
                species = Species.objects.get(code="BF")
            else:
                species = sire.species

            chick = Animal(species=species,
                           sex='U',
                           nest=self.cleaned_data['nest'],
                           hatch_date=self.cleaned_data['hatch_date'])
            chick.save()
            chick.update_age_days()
            Parent.objects.create(child=chick, parent=sire)
            Parent.objects.create(child=chick, parent=dam)

            GeneticParent.objects.create(genchild=chick, genparent=geneticsire)
            GeneticParent.objects.create(genchild=chick, genparent=geneticdam)


            chick.save()
            evt = Event(animal=chick,
                        date=self.cleaned_data['hatch_date'],
                        status=self.cleaned_data['status'],
                        description=self.cleaned_data['comments'],
                        location=self.cleaned_data['nest'],
                        entered_by=self.cleaned_data['user'])
            evt.save()
            ret['chicks'].append(chick)
            ret['events'].append(evt)
        return ret

class EggForm(forms.Form):
    sire = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='M'), required=False)
    dam  = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='F'), required=False)
    #geneticsire = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='M'), required=False)
    #geneticdam  = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='F'), required=False)      
    nest = forms.ModelChoiceField(queryset=Nest.objects.all())
    egg_number = forms.IntegerField(min_value=1)
    lay_date = forms.DateField(initial=datetime.date.today)
    comments = forms.CharField(widget=forms.Textarea, required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all())

    def clean(self):
        super(EggForm, self).clean()
        try:
            #ipdb.set_trace()
            self.cleaned_data['egg_event_code'] = EggEventCode.objects.get(name__startswith="laid")
        except:
            raise forms.ValidationError("No 'laid' status type - add one in admin")

        #if ('dam' in self.cleaned_data and 'sire' in self.cleaned_data and
        #    self.cleaned_data['dam'].species != self.cleaned_data['sire'].species):
        #    raise forms.ValidationError("Parents must be the same species")
        return self.cleaned_data


    def create_eggs(self):
        ret = {'eggs': [], 'events': []}
        
        for i in range(self.cleaned_data['egg_number']):

            if self.cleaned_data['nest'] is not None:
                nest_obj = Nest.objects.filter(name=self.cleaned_data['nest'])[0]
                sire = nest_obj.current_mating().sire
                dam = nest_obj.current_mating().dam
                   
            if self.cleaned_data['sire'] is not None:
                sire = self.cleaned_data['sire']

            if self.cleaned_data['dam'] is not None:
                sire = self.cleaned_data['dam']

            if sire is None:
                species = Species.objects.get(code="BF")
            else:
                species = sire.species

            egg = Egg(species=species,
                      sire = sire,
                      dam = dam,
                      nest=self.cleaned_data['nest'],
                      lay_date=self.cleaned_data['lay_date'])
            egg.save()
            ParentEgg.objects.create(egg=egg, parent=sire)
            ParentEgg.objects.create(egg=egg, parent=dam)

            egg.save()
            evt = EggEvent(egg=egg,
                        date=self.cleaned_data['lay_date'],
                        event=self.cleaned_data['egg_event_code'],
                        description=self.cleaned_data['comments'],
                        entered_by=self.cleaned_data['user'])
            evt.save()
            ret['eggs'].append(egg)
            ret['events'].append(evt)
        return ret

class AnimalSearchForm(forms.Form):
    acq_status = forms.ModelChoiceField(queryset=Status.objects.filter(count=1), required=False)
    sex = forms.ChoiceField(choices=(('M', 'male'),
                                     ('F', 'female'),
                                     ('U', 'unknown'),
                                     (None, 'all')), required=False, initial=None)
    alive = forms.ChoiceField(choices= ((True, 'yes'),
                                        (False, 'no'),
                                        (None, 'all')), required=False, initial=True)
    Nest = forms.ModelChoiceField(queryset=Nest.objects.all(), required=False)
    sire = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='M'),
                                  required=False)
    dam  = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='F'),
                                  required=False)
    species = forms.ModelChoiceField(queryset=Species.objects.all(), required=False)
    repeats = forms.ChoiceField(choices=(('yes','Y'),('no','N'),(None, 'all')),required=False,initial=None)
    seqvar = forms.ChoiceField(choices=(('yes','Y'),('no','N'),(None, 'all')),required=False,initial=None)
    banding_date = forms.DateField(required=False)
    colorband = forms.CharField(widget=forms.TextInput(), required=False)
    color1 = forms.ModelChoiceField(queryset=Color.objects.all(), required=False)
    color2 = forms.ModelChoiceField(queryset=Color.objects.all(), required=False)
    band1 = forms.IntegerField(required=False)
    band2 = forms.IntegerField(required=False)
    song_speed_greaterthan = forms.FloatField(required=False) #,queryset=Animal.objects.filter(song_speed__gte)
    song_speed_lessthan = forms.FloatField(required=False)
    call_speed_greaterthan = forms.FloatField(required=False) #,queryset=Animal.objects.filter(song_speed__gte)
    call_speed_lessthan = forms.FloatField(required=False)    
    call_speed = forms.FloatField(required=False)
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=False, to_field_name='name')
    comments = forms.CharField(widget=forms.Textarea, required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    reserved_by = forms.ModelChoiceField(queryset=User.objects.all(), required=False, to_field_name='username')

    def clean(self):
        super(AnimalSearchForm, self).clean()
        data = {}
        for key, val in self.cleaned_data.items():
            if not (val is None or val == ''):
                data[key] = val
        print(self.cleaned_data)
        print(data)
        return data

    class Meta:
        model = Animal
        #fields = ['hatch_date']

class AnimalForm(forms.ModelForm):

    ## Fields specified here to allow required=False
    sex = forms.ChoiceField(choices=(('M', 'male'),
                                     ('F', 'female'),
                                     ('U', 'unknown'),
                                     (None, 'all')), required=False)


    reserved_by = forms.ModelChoiceField(queryset=User.objects.all(),
                                         required=False,
                                         to_field_name='username')

    notes = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self):

        super(AnimalForm, self).clean()
        data = {}
        for key, val in self.cleaned_data.items():
            if not (val is None or val == ''):
                data[key] = val

        ## Also setting claim to blank
        if not 'reserved_by' in data:
            data['reserved_by'] = None

        ## Setting date of action
        if not 'date' in data:
            data['date'] = datetime.date.today

        return data

    def update_claims(self, animal):
        claim = Claim(animal = animal,
                      username = self.cleaned_data['reserved_by'],
                      date = self.cleaned_data['date']())
        claim.save()

    class Meta:
        model = Animal
        fields = ['sex', 'reserved_by', 'notes']

class NestForm(forms.ModelForm):

    ## Fields specified here to allow required=False
    notes = forms.CharField(widget=forms.Textarea, required=False)
    reserved_by = forms.ModelChoiceField(queryset=User.objects.all(),
                                          required=False,
                                         to_field_name='username')

    def clean(self):
        super(NestForm, self).clean()
        data = {}
        for key, val in self.cleaned_data.items():
            if not (val is None or val == ''):
                data[key] = val

        ## Also setting claim to blank
        if not 'reserved_by' in data:
            data['reserved_by'] = None

        ## Setting date of action
        #if not 'date' in data:
        #    data['date'] = datetime.date.today

        return data

    # def update_claims(self, animal):
    #     claim = Claim(animal = animal,
    #                   username = self.cleaned_data['reserved_by'],
    #                   date = self.cleaned_data['date']())
    #     claim.save()

    class Meta:
        model = Nest
        fields = [ 'reserved_by', 'notes']

class MatingEntryForm(forms.ModelForm):

    nest = forms.ModelChoiceField(queryset=Nest.objects.all(), required=False)
    sire = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='M'),
                                  required=False)
    dam  = forms.ModelChoiceField(queryset=Animal.objects.filter(sex__exact='F'),
                                  required=False)
    entered_by = forms.ModelChoiceField(queryset=User.objects.all())
    created = forms.DateField(required=True)

    class Meta:
        model = Mating
        fields = ['nest', 'sire', 'dam']
