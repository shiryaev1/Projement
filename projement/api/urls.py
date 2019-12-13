from django.urls import path, re_path

from api.views import DashboardViewSet, ProjectUpdateView, CompanyCreateView, \
    ProjectCreateView, HistoryOfChangesListView, HistoryOfChangesDetailListView, \
    TagCreateView, TagUpdateView, TagDeleteView

app_name = 'api'

urlpatterns = [
    path('dashboard/', DashboardViewSet.as_view({'get': 'list'}),
         name='dashboard'),
    path('company/create/', CompanyCreateView.as_view(), name='company-create'),
    path('project/create/', ProjectCreateView.as_view(), name='project-create'),
    re_path('^project/(?P<id>[0-9]+)/update/$', ProjectUpdateView.as_view(),
            name='project-update'),
    path('project/history/', HistoryOfChangesListView.as_view(),
         name='project-history'),
    re_path('^project/(?P<pk>[0-9]+)/history/(?P<id>[0-9]+)/$',
            HistoryOfChangesDetailListView.as_view(),
            name='project-history-detail'),
    path('tag/create/',  TagCreateView.as_view(), name='tag-create'),
    re_path('^tag/(?P<id>[0-9]+)/update/$', TagUpdateView.as_view(),
            name='tag-update'),
    re_path('^tag/(?P<id>[0-9]+)/delete/$', TagDeleteView.as_view(),
            name='tag-delete'),
]