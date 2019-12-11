import decimal
import os
import pdb

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView

from markdown import markdown
from itertools import chain

from projects.filters import ProjectFilter
from projects.forms import ProjectForm, TagForm, ProjectCreateForm
from projects.models import Project, Tag, HistoryOfChanges, InitialDataOfProject


class AssignmentView(TemplateView):
    template_name = 'projects/assignment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with open(os.path.join(os.path.dirname(settings.BASE_DIR), 'README.md'), encoding='utf-8') as f:
            assignment_content = f.read()

        context.update({
            'assignment_content': mark_safe(markdown(assignment_content))
        })

        return context


class DashboardView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/dashboard.html'

    def get_queryset(self):
        end_projects = Project.objects.filter(
            end_date__isnull=False).order_by('-end_date')
        active_projects = Project.objects.filter(end_date__isnull=True).order_by('-start_date')
        projects = list(chain(active_projects, end_projects))

        return projects


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    success_url = reverse_lazy('dashboard')


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):

        original = Project.objects.get(pk=kwargs['pk'])
        # original.additional_hour_design += Project.objects.get(
        #     id=original.id
        # ).additional_hour_design + decimal.Decimal(request.POST['actual_design'])

        if float(original.actual_testing) != float(request.POST['actual_testing']) \
                or float(original.actual_development) != float(request.POST['actual_development']) \
                or float(original.actual_design) != float(request.POST['actual_design']):

            HistoryOfChanges.objects.get_or_create(
                change_delta_actual_design=float(request.POST['actual_design']) - float(original.actual_design),
                resulting_actual_design=float(request.POST['actual_design']),
                change_delta_actual_development=float(request.POST['actual_development']) - float(original.actual_development),
                resulting_actual_development=float(request.POST['actual_development']),
                change_delta_actual_testing=float(request.POST['actual_testing']) - float(original.actual_testing),
                resulting_actual_testing=float(request.POST['actual_testing']),
                change_time=timezone.now(),
                project=original,
                owner=request.user
            )

        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            if request.POST['additional_hour_design']:
                original.actual_design += decimal.Decimal(
                    request.POST['additional_hour_design'])
            if request.POST['additional_hour_testing']:
                original.actual_testing += decimal.Decimal(
                    request.POST['additional_hour_testing'])
            if request.POST['additional_hour_development']:
                original.actual_development += decimal.Decimal(
                request.POST['additional_hour_development'])
            original.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class HistoryOfChangesView(LoginRequiredMixin, ListView):
    model = HistoryOfChanges
    context_object_name = 'history_of_changes'
    template_name = 'projects/history_of_changes.html'

    def get_context_data(self, **kwargs):
        context = super(HistoryOfChangesView, self).get_context_data(**kwargs)
        context['filter'] = ProjectFilter(self.request.GET, queryset=self.get_queryset().order_by('-id'))
        return context


class HistoryOfChangesDetailView(LoginRequiredMixin, ListView):
    template_name = 'projects/project_changes.html'
    model = HistoryOfChanges
    context_object_name = 'history_of_changes'

    def get_queryset(self):
        history_of_changes = HistoryOfChanges.objects.filter(
            id=self.request.resolver_match.kwargs['pk']
        )
        initial_data = InitialDataOfProject.objects.filter(
            project__id=self.request.resolver_match.kwargs['id'])
        return history_of_changes

    def get_context_data(self, **kwargs):
        context = super(HistoryOfChangesDetailView, self).get_context_data(**kwargs)
        context['initial_data'] = InitialDataOfProject.objects.filter(
            project__id=self.request.resolver_match.kwargs['id'])
        return context


class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'projects/tag_create.html'
    reverse_lazy = 'tag-list'


class TagEditView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'projects/tag_edit.html'
    reverse_lazy = 'tag-list'


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'projects/tag_delete.html'
    success_url = reverse_lazy('tag-list')


def tags_list_view(request):
    tags = Tag.objects.all()
    return render(request, 'projects/tags_list.html', {'tags': tags})

