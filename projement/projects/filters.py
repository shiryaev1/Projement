import  django_filters
from projects.models import HistoryOfChanges


class ProjectFilter(django_filters.FilterSet):

    class Meta:
        model = HistoryOfChanges
        fields = ('project__title', )
