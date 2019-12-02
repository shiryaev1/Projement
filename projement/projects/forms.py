from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from projects.models import Project, Tag


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['actual_design', 'actual_development', 'actual_testing']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'UPDATE'))


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }