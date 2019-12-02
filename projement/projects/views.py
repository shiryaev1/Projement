import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from operator import attrgetter
from markdown import markdown
from itertools import chain
from projects.forms import ProjectForm, TagForm
from projects.models import Project, Tag


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
        active_projects = Project.objects.select_related('company').exclude(
            end_date__isnull=False).order_by('-start_date')
        end_projects = Project.objects.exclude(end_date__isnull=True).order_by('-end_date')
        projects = list(chain(active_projects, end_projects))

        return projects


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('dashboard')


class TagCreate(View):
    def get(self,request):
        form = TagForm()
        args = {'form': form}
        return render(request, 'projects/tag_create.html', args)

    def post(self,request):
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_create_url')
        args = {'form': form}
        return render(request, 'projects/tag_create.html', args)


class TagEditView(View):

    template_name = 'projects/tag_edit.html'

    def get(self, request, id):
        try:
            tag = Tag.objects.get(id=id)
        except ObjectDoesNotExist:
            raise Http404
        form = TagForm(instance=tag)
        args = {
            'form': form,
        }
        return render(request, self.template_name, args)

    def post(self, request, id):
        try:
            tag = Tag.objects.get(id=id)
        except ObjectDoesNotExist:
            return Http404
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('tag_create_url')
        args = {
            'form': form
        }
        return render(request, self.template_name, args)


def tags_list_view(request):
    tags = Tag.objects.all()
    return render(request, 'projects/tags_list.html', {'tags': tags})