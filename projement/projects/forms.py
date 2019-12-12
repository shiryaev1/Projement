import pdb

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django.db.models import F
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'CREATE'))

    def save(self, commit=True):
        project = super(ProjectCreateForm, self).save(commit=False)
        project.save()
        initial_data_of_project = InitialDataOfProject.objects.get_or_create(
            initial_actual_design=project.actual_design,
            initial_actual_development=project.actual_development,
            initial_actual_testing=project.actual_testing,
            project=project
        )
        if self.cleaned_data['tags']:
            data_of_tag = DataOfTag.objects.create(
                tag=self.cleaned_data.get('tags')._result_cache,
                project=project,
                time_to_add=timezone.now(),
            )

        return project


class ProjectForm(forms.ModelForm):
    additional_hour_design = forms.DecimalField(required=False)
    additional_hour_development = forms.DecimalField(required=False)
    additional_hour_testing = forms.DecimalField(required=False)

    class Meta:
        model = Project
        fields = [
            'actual_design',
            'actual_development',
            'actual_testing',
            'additional_hour_design',
            'additional_hour_development',
            'additional_hour_testing',
            'tags',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'UPDATE'))

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        if self.instance.pk is not None:
            if self.initial['tags'] != list(cleaned_data['tags']):
                DataOfTag.objects.create(
                    tag=list(cleaned_data['tags']),
                    project=self.instance,
                    time_to_add=timezone.now(),
                )
        return cleaned_data


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'CREATE'))