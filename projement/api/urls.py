from django.urls import path, re_path

from api.views import DashboardViewSet, ProjectUpdateView, CompanyCreateView, \
    ProjectCreateView

app_name = 'api'

urlpatterns = [
    path('dashboard/', DashboardViewSet.as_view({'get': 'list'}),
         name='dashboard'),
    path('company/create/', CompanyCreateView.as_view(), name='company-create'),
    path('project/create/', ProjectCreateView.as_view(), name='project-create'),
    re_path('^project/(?P<id>[0-9]+)/update/$', ProjectUpdateView.as_view(),
            name='project-update')

]