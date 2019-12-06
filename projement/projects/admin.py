from django.contrib import admin

from projects.models import Company, Project, Tag, DataOfTag, HistoryOfChanges, \
    InitialDataOfProject


class DecadeBornListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('actual company')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'company'

    def lookups(self, request, model_admin):
        projects = list(Project.objects.all())
        return set([(project.company.id, project.company.name) for project in projects])

    def queryset(self, request, queryset):
        projects = list(Project.objects.all())
        pass



class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date',)
    list_filter = ('company__name',  DecadeBornListFilter   )
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
     ('Additional hours', {'fields': [
         'additional_hour_design',
         'additional_hour_development',
         'additional_hour_testing'
     ]})
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