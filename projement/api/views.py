from django.contrib.auth import authenticate, login
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.generics import RetrieveUpdateAPIView, \
    get_object_or_404, ListAPIView, RetrieveAPIView, \
    ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsReadOnly
from api.serializers import DashboardListSerializer, ProjectUpdateSerializer, \
    CompanyCreateSerializer, ProjectCreateSerializer, \
    HistoryOfChangesSerializer, HistoryOfChangesDetailSerializer, TagSerializer, \
    TagAddingHistorySerializer, InitialDataOfProjectSerializer, \
    UserLoginSerializer
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


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @staticmethod
    def post(request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if user is None or not user.is_active:
            return Response({
                'message': 'Username or password incorrect'
            }, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        return Response(UserLoginSerializer(user).data)