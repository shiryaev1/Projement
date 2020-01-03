
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from rest_framework.generics import RetrieveUpdateAPIView, \
    get_object_or_404, ListAPIView, RetrieveAPIView, \
    ListCreateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from knox.models import AuthToken

from api.permissions import IsReadOnly
from api.serializers import DashboardListSerializer, ProjectUpdateSerializer, \
    CompanyCreateSerializer, ProjectCreateSerializer, \
    HistoryOfChangesSerializer, HistoryOfChangesDetailSerializer, TagSerializer, \
    TagAddingHistorySerializer, InitialDataOfProjectSerializer, \
    UserSerializer, RegisterSerializer, LoginSerializer
from projects.models import Project, HistoryOfChanges, Tag, TagAddingHistory, \
    InitialDataOfProject, Company


class DashboardViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardListSerializer
    queryset = Project.objects.order_by(
            F('end_date').desc(nulls_first=True))
    # permission_classes = [IsReadOnly, IsAuthenticated]


class ProjectUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProjectUpdateSerializer
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs["id"]
        return get_object_or_404(Project, id=pk)


class CompanyCreateView(ListCreateAPIView):
    serializer_class = CompanyCreateSerializer
    queryset = Company.objects.all()
    # permission_classes = [IsAuthenticated]


class ProjectCreateView(ListCreateAPIView):
    serializer_class = ProjectCreateSerializer
    # permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()


class HistoryOfChangesListView(ListAPIView):
    serializer_class = HistoryOfChangesSerializer
    queryset = HistoryOfChanges.objects.order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project__title', ]
    # permission_classes = [IsAuthenticated]


class HistoryOfChangesDetailListView(RetrieveAPIView):
    serializer_class = HistoryOfChangesDetailSerializer
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = HistoryOfChanges.objects.filter(
            id=self.kwargs['id']
        )
        return queryset


class TagCreateView(ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    # permission_classes = [IsAuthenticated]


class TagUpdateView(RetrieveUpdateAPIView):
    serializer_class = TagSerializer
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Tag.objects.filter(
            id=self.kwargs['id']
        )
        return queryset


class TagDeleteView(DestroyAPIView):
    serializer_class = TagSerializer
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Tag.objects.filter(
            id=self.kwargs['id']
        )
        return queryset


class TagAddingHistoryView(ListAPIView):
    serializer_class = TagAddingHistorySerializer
    queryset = TagAddingHistory.objects.all()
    permission_classes = [IsAuthenticated]


class InitialDataOfProjectView(viewsets.ModelViewSet):
    serializer_class = InitialDataOfProjectSerializer
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = InitialDataOfProject.objects.filter(
            project__id=self.kwargs['id']
        )
        return queryset


class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,
                                   context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
          "user": UserSerializer(user,
                                 context=self.get_serializer_context()).data,
          "token": AuthToken.objects.create(user)[1]
        })


class UserAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user