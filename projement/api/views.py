from django.db.models import F
from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView, RetrieveUpdateAPIView, \
    get_object_or_404, CreateAPIView

from api.permissions import IsReadOnly
from api.serializers import DashboardListSerializer, ProjectUpdateSerializer, \
    CompanyCreateSerializer, ProjectCreateSerializer
from projects.models import Project


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
