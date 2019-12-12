
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms.utils import flatatt
from django.utils import timezone
from django.utils.safestring import mark_safe

from projects.models import Project, Tag, TagAddingHistory


class TagChangeListForm(forms.CheckboxSelectMultiple):
    def __init__(self, attrs=None, ul_attrs=None):
        self.ul_attrs = ul_attrs
        super(TagChangeListForm, self).__init__(attrs)

    def render(self, name, value, attrs=None, choices=()):
        html = super(TagChangeListForm, self).render(name, value, attrs, choices)
        final_attrs = self.build_attrs(self.ul_attrs)
        return mark_safe(html.replace('<ul>','<ul%s>' % flatatt(final_attrs)))


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