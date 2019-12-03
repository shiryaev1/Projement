from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from projects.models import Company, Project, Tag, DataOfTag, HistoryOfChanges


# class CustomRelatedOnlyFieldListFilter(admin.SimpleListFilter):
#     title = 'id'
#     parameter_name = 'id'
#     def lookups(self, request, model_admin):
#         companies = Company.objects.values_list('name')
#         for company in companies:
#             return company
#     def queryset(self, request, queryset):
#         return Project.objects.all()

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date',)
    # list_filter = ('company__name', CustomRelatedOnlyFieldListFilter)
    ordering = ('-start_date',)

    fieldsets = (
        (None, {'fields': ['company', 'title', 'start_date', 'end_date', 'tags',]}),
        ('Estimated hours', {'fields': ['estimated_design', 'estimated_development', 'estimated_testing',]}),
        ('Actual hours', {'fields': ['actual_design', 'actual_development', 'actual_testing']}),
        ('Additional hours', {'fields': ['additional_hour_design', 'additional_hour_development', 'additional_hour_testing']})
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
            'initial_actual_design',
            'change_delta_actual_design',
            'resulting_actual_design',
        ]}),
        ('Development', {'fields': [
            'initial_actual_development',
            'change_delta_actual_development',
            'resulting_actual_development'
        ]}),
        ('Testing', {'fields': [
            'initial_actual_testing',
            'change_delta_actual_testing',
            'resulting_actual_testing'
        ]})
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