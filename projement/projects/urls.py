from django.conf.urls import url
from projects import views
from projects.views import AssignmentView, DashboardView, ProjectUpdateView, \
    TagCreate, TagEditView

urlpatterns = [
    url(r'^$', AssignmentView.as_view(), name='assignment'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^projects/(?P<pk>[0-9]+)-(?P<slug>[-\w]*)/$', ProjectUpdateView.as_view(), name='project-update'),
    url(r'^tag/create/$', TagCreate.as_view(), name='tag_create_url'),
    url(r'^tag/(?P<id>\d+)/edit/$', TagEditView.as_view(), name='tag-edit'),
    url(r'^tags/$', views.tags_list_view, name='tag-list')
]
