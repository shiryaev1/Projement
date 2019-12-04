import pdb

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django.utils import timezone

from projects.models import Project, Tag, DataOfTag, InitialDataOfProject


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'company',
            'title',
            'start_date',
            'end_date',
            'estimated_design',
            'actual_design',
            'estimated_development',
            'actual_development',
            'estimated_testing',
            'actual_testing',
            'tags',
        )

    def save(self, commit=True):
        projects = super(ProjectCreateForm, self).save(commit=False)
        projects.save()
        initial_data_of_project = InitialDataOfProject.objects.get_or_create(
            initial_actual_design=projects.actual_design,
            initial_actual_development=projects.actual_development,
            initial_actual_testing=projects.actual_testing,
            project=projects
        )
        if self.data['tags']:
            data_of_tag = DataOfTag.objects.create(
                tag=projects.tags,
                project=projects,
                time_to_add=timezone.now(),
            )

        return projects


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'additional_hour_design',
            'additional_hour_development',
            'additional_hour_testing',
            'tags',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'UPDATE'))

    def save(self, commit=True):
        projects = super(ProjectForm, self).save(commit=False)
        projects.save()
        if self.data['tags']:
            tag__in = self.data['tags']
            print(tag__in)
            data_of_tag = DataOfTag.objects.create(
                # pdb.set_trace(),
                tag=self.cleaned_data.get('tags')._result_cache,
                project=projects,
                time_to_add=timezone.now(),
            )

        return projects


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title',]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }