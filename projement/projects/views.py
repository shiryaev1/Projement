import decimal
import os

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

from projects.filters import ProjectFilter
from projects.forms import ProjectForm, TagForm, ProjectCreateForm
from projects.models import Project, Tag, HistoryOfChanges, \
    InitialDataOfProject, TagAddingHistory


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
        projects = Project.objects.order_by(
            F('end_date').desc(nulls_first=True))
        return projects


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            InitialDataOfProject.objects.get_or_create(
                initial_actual_design=form.cleaned_data['actual_design'],
                initial_actual_development=form.cleaned_data['actual_development'],
                initial_actual_testing=form.cleaned_data['actual_testing'],
                project=self.object
            )
            TagAddingHistory.objects.create(
                tag=list(form.cleaned_data.get('tags')),
                project=self.object,
                time_to_add=timezone.now(),
            )
            return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        original = Project.objects.get(pk=kwargs['pk'])

        if str(
            request.POST['additional_hour_testing']) != '0' \
            or str(
            request.POST['additional_hour_development']) != '0' \
            or str(
            request.POST['additional_hour_design']) != '0':

            HistoryOfChanges.objects.get_or_create(
                change_delta_actual_design=decimal.Decimal(
                    request.POST['additional_hour_design']
                ),
                resulting_actual_design=decimal.Decimal(
                    request.POST['additional_hour_design']) + original.actual_design,

                change_delta_actual_development=decimal.Decimal(
                    request.POST['additional_hour_development']),

                resulting_actual_development=decimal.Decimal(
                    request.POST['additional_hour_development']) + original.actual_development,

                change_delta_actual_testing=decimal.Decimal(
                    request.POST['additional_hour_testing']),

                resulting_actual_testing=decimal.Decimal(
                    request.POST['additional_hour_testing']) + original.actual_testing,
                change_time=timezone.now(),
                project=original,
                owner=request.user
            )
        return super(ProjectUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = self.get_object()
        form = self.get_form()
        original = Project.objects.get(pk=self.object.pk)

        if form.is_valid():

            if list(original.tags.distinct()) != list(
                    form.cleaned_data['tags']):
                TagAddingHistory.objects.create(
                    tag=list(form.cleaned_data['tags']),
                    project=self.object,
                    time_to_add=timezone.now(),
                )
            self.object = form.save()

            if form.cleaned_data['additional_hour_design']:
                original.actual_design += decimal.Decimal(
                    form.cleaned_data['additional_hour_design'])
            if form.cleaned_data['additional_hour_testing']:
                original.actual_testing += decimal.Decimal(
                    form.cleaned_data['additional_hour_testing'])
            if form.cleaned_data['additional_hour_development']:
                original.actual_development += decimal.Decimal(
                    form.cleaned_data['additional_hour_development'])
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


class TagAddingHistoryView(LoginRequiredMixin, ListView):
    template_name = 'projects/tag_adding_history.html'
    model = TagAddingHistory
    context_object_name = 'tag_adding_history'


def tags_list_view(request):
    tags = Tag.objects.all()
    return render(request, 'projects/tags_list.html', {'tags': tags})

