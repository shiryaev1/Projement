from django.urls import path, re_path

from api.views import DashboardViewSet, ProjectUpdateView

app_name = 'api'

urlpatterns = [
    path('dashboard/', DashboardViewSet.as_view({'get': 'list'}),
         name='dashboard'),
    re_path('^project/(?P<id>[0-9]+)/update/$', ProjectUpdateView.as_view(),
            name='project-update')

]