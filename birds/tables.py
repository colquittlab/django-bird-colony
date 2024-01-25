from django.db.models import Min
import django_tables2 as tables
from .models import Animal, Nest, Mating, Egg

class AnimalTable(tables.Table):

    # see https://django-tables2.readthedocs.io/en/latest/pages/ordering.html
    band = tables.Column(order_by=('band_color', 'band_number', 'band_color2', 'band_number2'))

    def order_age_days(self, queryset, is_descending):
       queryset = queryset.order_by(('-' if is_descending else '') + 'hatch_date')
       return (queryset, True)

    edit = tables.TemplateColumn('<a href="/birds/animals/{{record.uuid}}">View</a>')
    class Meta:
        model = Animal
        template = 'django_tables2/bootstrap.html'
        sequence = ('band', 'sex', 'age_days', 'hatch_date', 'alive', 'location', 'nest', 'reserved_by','song_speed','call_speed','seqvar','repeats','notes', 'edit')
        fields = ('band', 'sex', 'age_days', 'hatch_date', 'alive', 'location', 'nest', 'reserved_by','song_speed','call_speed','seqvar','repeats', 'notes','edit')

class NestTable(tables.Table):
    edit = tables.TemplateColumn('<a href="/birds/nests/{{record.uuid}}">View</a>')

    class Meta:
        model = Nest
        template = 'django_tables2/bootstrap.html'
        sequence = ('name', 'sire', 'dam', 'created', 'reserved_by', 'nest_bands1', 'nest_bands2', 'current_egg_number', 'current_hatchling_number', 'notes', 'edit')
        fields = ('name', 'sire', 'dam', 'created', 'reserved_by', 'nest_bands1', 'nest_bands2', 'current_egg_number', 'current_hatchling_number', 'notes', 'edit')

class MatingTable(tables.Table):
    edit = tables.TemplateColumn('<a href="/birds/matings/{{record.uuid}}">View</a>')

    class Meta:
        model = Mating
        template = 'django_tables2/bootstrap.html'
        sequence = ('nest', 'sire', 'dam', 'created')
        fields = ('nest', 'sire', 'dam', 'created')

class EggTable(tables.Table):
    edit = tables.TemplateColumn('<a href="/birds/eggs/{{record.uuid}}">View</a>')

    class Meta:
        model = Egg
        template = 'django_tables2/bootstrap.html'
        sequence = ('nest', 'sire', 'dam', 'lay_date', 'created')
        fields = ('nest', 'sire', 'dam', 'lay_date', 'created')
