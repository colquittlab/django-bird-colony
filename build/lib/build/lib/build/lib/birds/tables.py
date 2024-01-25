from django.db.models import Min
import django_tables2 as tables
from .models import Animal, Nest

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
        sequence = ('band', 'sex', 'age_days', 'hatch_date', 'alive', 'last_location', 'nest', 'reserved_by','song_speed','call_speed','seqvar','repeats','notes', 'edit')
        fields = ('band', 'sex', 'age_days', 'hatch_date', 'alive', 'last_location', 'nest', 'reserved_by','song_speed','call_speed','seqvar','repeats', 'notes','edit')

class NestTable(tables.Table):
    edit = tables.TemplateColumn('<a href="/birds/nests/{{record.uuid}}">View</a>')

    class Meta:
        model = Nest
        template = 'django_tables2/bootstrap.html'
        sequence = ('name', 'sire', 'dam', 'created', 'nest_bands', 'uuid', 'edit')
        fields = ('name', 'sire', 'dam', 'created', 'nest_bands', 'uuid', 'edit')
