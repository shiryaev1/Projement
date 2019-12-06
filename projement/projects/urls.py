from django.conf.urls import url
from django.urls import path

from projects import views
from projects.views import AssignmentView, DashboardView, ProjectUpdateView, \
    TagCreate, TagEditView, TagDeleteView, ProjectCreateView
from projects.export import export_projects_xls

urlpatterns = [
    url(r'^$', AssignmentView.as_view(), name='assignment'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^projects/create/$', ProjectCreateView.as_view(), name='project-create'),
    url(r'^projects/(?P<pk>[0-9]+)-(?P<slug>[-\w]*)/$', ProjectUpdateView.as_view(), name='project-update'),
    url(r'^tag/create/$', TagCreate.as_view(), name='tag_create_url'),
    url(r'^tag/(?P<pk>\d+)/edit/$', TagEditView.as_view(), name='tag-edit'),
    url(r'^tag/(?P<pk>\d+)/delete/$', TagDeleteView.as_view(), name='tag-delete'),
    url(r'^tags/$', views.tags_list_view, name='tag-list'),
    url(r'^export/excel/$', export_projects_xls, name='export_excel')
]
