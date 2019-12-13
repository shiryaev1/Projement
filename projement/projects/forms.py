
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms.utils import flatatt
from django.utils import timezone
from django.utils.safestring import mark_safe

from projects.models import Project, Tag, TagAddingHistory


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


class ProjectForm(forms.ModelForm):
    additional_hour_design = forms.DecimalField(required=False, initial=0)
    additional_hour_development = forms.DecimalField(required=False, initial=0)
    additional_hour_testing = forms.DecimalField(required=False, initial=0)

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
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['actual_design'].widget.attrs['readonly'] = True
            self.fields['actual_development'].widget.attrs['readonly'] = True
            self.fields['actual_testing'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'UPDATE'))


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'CREATE'))