from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django.utils import timezone

from projects.models import Project, Tag, DataOfTag


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
        data_of_tag = DataOfTag.objects.create(
            tag=projects.tags,
            project=projects,
            time_to_add=timezone.now(),
        )

        return data_of_tag


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

        data_of_tag = DataOfTag.objects.create(
            tag=projects.tags,
            project=projects,
            time_to_add=timezone.now(),
        )

        return data_of_tag


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title',]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }