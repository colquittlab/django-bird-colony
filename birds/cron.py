import datetime
from birds.models import Animal
from django.db.models import Max, Min, F

def update_all_age_days():

    
    qs_alive = Animal.objects.filter(alive=True)
    qs = Animal.objects.all()
    for animal in qs.iterator():
        update_age_days(animal)
    #q_birth = qs_alive.event_set.filter(status__name="hatched").aggregate(d=Min("date"))
    #if animal.alive:
    #qs_alive.update(age_days = (datetime.date.today() - q_birth["d"]).days)
    #qs_alive.update(age_days = (datetime.date.today() - F('hatch_date')))

    #qs_dead = Animal.objects.filter(alive=False)
    #else:
    #q_death = qs_dead.filter(status__count__lt=0).aggregate(d=Max("date"))
    #qs_dead.update(age_days = (q_death["d"] - q_birth["d"]).days)
        
    
        
def update_age_days(animal):
    
    """ Returns days since birthdate if alive, age at death if dead, or None if unknown"""
    q_birth = animal.event_set.filter(status__name="hatched").aggregate(d=Min("date"))
    print(animal.band)
    if q_birth["d"] is None:
        return None
    if animal.alive:
        animal.age_days = (datetime.date.today() - q_birth["d"]).days
    else:
        q_death = animal.event_set.filter(status__count__lt=0).aggregate(d=Max("date"))
        animal.age_days = (q_death["d"] - q_birth["d"]).days

    animal.save()
