from celery.schedules import crontab
from celery.task import periodic_task
from models import Animal

@periodic_task(run_every=crontab(hour=0, minute=30))
def update_age_days_all():
    qs = Animal.objects.all()
    [q.update_age_days() for q in qs]

