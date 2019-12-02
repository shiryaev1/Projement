from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from projects.models import Company, Project


class CountryFilter(SimpleListFilter):
    title = 'company__name'
    parameter_name = 'company__name'

    def lookups(self, request, model_admin):
        companies = Company.objects.all().values()
        return companies

    def queryset(self, request, queryset):
        queryset = Project.objects.filter()
        return queryset


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date')
    # list_filter = ('company__name', 'company__id')
    ordering = ('-start_date',)
    list_filter = (CountryFilter, )

    fieldsets = (
        (None, {'fields': ['company', 'title', 'start_date', 'end_date']}),
        ('Estimated hours', {'fields': ['estimated_design', 'estimated_development', 'estimated_testing']}),
        ('Actual hours', {'fields': ['actual_design', 'actual_development', 'actual_testing']}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()

        return 'company',


admin.site.register(Company)
admin.site.register(Project, ProjectAdmin)
