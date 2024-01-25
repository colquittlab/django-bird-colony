import datetime
from birds.models import Animal
from django.db.models import Max, Min, F

def update_all_age_days():

    
    qs_alive = Animal.objects.filter(alive=True)
    qs = Animal.objects.all()
    for animal in qs.iterator():
        animal.update_age_days()        
        
# def update_age_days(animal):
    
#     """ Returns days since birthdate if alive, age at death if dead, or None if unknown"""
#     q_birth = animal.event_set.filter(status__name="hatched").aggregate(d=Min("date"))
#     print(animal.band)
#     if q_birth["d"] is None:
#         return None
#     if animal.alive:
#         animal.age_days = (datetime.date.today() - q_birth["d"]).days
#     else:
#         q_death = animal.event_set.filter(status__count__lt=0).aggregate(d=Max("date"))
#         animal.age_days = (q_death["d"] - q_birth["d"]).days

#     animal.save()
