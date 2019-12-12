
from django.contrib import admin

from projects.models import Company, Project, Tag, DataOfTag, HistoryOfChanges, \
    InitialDataOfProject


class ActualCompanyListFilter(admin.SimpleListFilter):

    title = 'actual company'

    parameter_name = 'company'

    def lookups(self, request, model_admin):
        projects = list(Project.objects.all())
        return set([(project.company.id, project.company.name) for project in projects])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(company__id__exact=self.value())


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date',)
    list_filter = ('company__name',  ActualCompanyListFilter,)
    ordering = ('-start_date',)

    fieldsets = (
     (None, {'fields': [
         'company',
         'title',
         'start_date',
         'end_date',
         'tags',
     ]}),
     ('Estimated hours', {'fields': [
         'estimated_design',
         'estimated_development',
         'estimated_testing',
     ]}),
     ('Actual hours', {'fields': [
         'actual_design',
         'actual_development',
         'actual_testing'
     ]}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()

        return 'company',


class HistoryOfChangesAdmin(admin.ModelAdmin):
    list_display = ('change_time', 'project', 'owner',)

    fieldsets = (
        (None, {'fields': ['change_time', 'project', 'owner', ]}),
        ('Design', {'fields': [
            'change_delta_actual_design',
            'resulting_actual_design',
        ]}),
        ('Development', {'fields': [
            'change_delta_actual_development',
            'resulting_actual_development'
        ]}),
        ('Testing', {'fields': [
            'change_delta_actual_testing',
            'resulting_actual_testing'
        ]})
        )


class InitialDataOfProjectAdmin(admin.ModelAdmin):
    list_display = ('project',)

    fieldsets = (
        (None, {'fields': [
            'initial_actual_design',
            'initial_actual_development',
            'initial_actual_testing',
            'project',
        ]}),

    )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()

        return 'initial_actual_design',\
               'initial_actual_development',\
               'initial_actual_testing'


admin.site.register(Company)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag)
admin.site.register(DataOfTag)
admin.site.register(HistoryOfChanges, HistoryOfChangesAdmin)
admin.site.register(InitialDataOfProject, InitialDataOfProjectAdmin)