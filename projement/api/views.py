from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView, RetrieveUpdateAPIView, \
    get_object_or_404, CreateAPIView, ListAPIView, RetrieveAPIView, \
    RetrieveUpdateDestroyAPIView, ListCreateAPIView, DestroyAPIView

from api.permissions import IsReadOnly
from api.serializers import DashboardListSerializer, ProjectUpdateSerializer, \
    CompanyCreateSerializer, ProjectCreateSerializer, \
    HistoryOfChangesSerializer, HistoryOfChangesDetailSerializer, TagSerializer, \
    TagAddingHistorySerializer, InitialDataOfProjectSerializer
from projects.models import Project, HistoryOfChanges, Tag, TagAddingHistory, \
    InitialDataOfProject


class DashboardViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardListSerializer
    queryset = Project.objects.order_by(
            F('end_date').desc(nulls_first=True))
    permission_classes = [IsReadOnly]


class ProjectUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProjectUpdateSerializer
    lookup_field = 'id'

    def get_object(self):
        pk = self.kwargs["id"]
        return get_object_or_404(Project, id=pk)


class CompanyCreateView(CreateAPIView):
    serializer_class = CompanyCreateSerializer


class ProjectCreateView(CreateAPIView):
    serializer_class = ProjectCreateSerializer


class HistoryOfChangesListView(ListAPIView):
    serializer_class = HistoryOfChangesSerializer
    queryset = HistoryOfChanges.objects.order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project__title', ]


class HistoryOfChangesDetailListView(RetrieveAPIView):
    serializer_class = HistoryOfChangesDetailSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = HistoryOfChanges.objects.filter(
            id=self.kwargs['id']
        )
        return queryset


class TagCreateView(ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class TagUpdateView(RetrieveUpdateAPIView):
    serializer_class = TagSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Tag.objects.filter(
            id=self.kwargs['id']
        )
        return queryset


class TagDeleteView(DestroyAPIView):
    serializer_class = TagSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Tag.objects.filter(
            id=self.kwargs['id']
        )
        return queryset


class TagAddingHistoryView(ListAPIView):
    serializer_class = TagAddingHistorySerializer
    queryset = TagAddingHistory.objects.all()


class InitialDataOfProjectView(viewsets.ModelViewSet):
    serializer_class = InitialDataOfProjectSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = InitialDataOfProject.objects.filter(
            project__id=self.kwargs['id']
        )
        return queryset
