from django.contrib.auth.models import User
from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Count, F
from projects.get_request import get_request


class Company(models.Model):

    class Meta:
        verbose_name_plural = "companies"

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Project(models.Model):

    company = models.ForeignKey('projects.Company', on_delete=models.PROTECT,
                                related_name='projects')

    title = models.CharField('Project title', max_length=128)
    start_date = models.DateField('Project start date', blank=True, null=True)
    end_date = models.DateField('Project end date', blank=True, null=True)

    estimated_design = models.DecimalField('Estimated design hours',
                                           max_digits=7, decimal_places=2,
                                           validators=[
                                               MaxValueValidator(10000),
                                               MinValueValidator(0),
                                           ]
                                           )
    actual_design = models.DecimalField('Actual design hours', default=0,
                                        max_digits=7, decimal_places=2,
                                        validators=[
                                            MaxValueValidator(10000),
                                            MinValueValidator(0),
                                        ]
                                        )

    estimated_development = models.DecimalField('Estimated development hours',
                                                max_digits=7, decimal_places=2,
                                                validators=[
                                                    MaxValueValidator(10000),
                                                    MinValueValidator(0),
                                                ]
                                                )
    actual_development = models.DecimalField('Actual development hours',
                                             default=0, max_digits=7,
                                             decimal_places=2,
                                             validators=[
                                                 MaxValueValidator(10000),
                                                 MinValueValidator(0),
                                             ]
                                             )

    estimated_testing = models.DecimalField('Estimated testing hours',
                                            max_digits=7, decimal_places=2,
                                            validators=[
                                                MaxValueValidator(10000),
                                                MinValueValidator(0),
                                            ]
                                            )
    actual_testing = models.DecimalField('Actual testing hours', default=0,
                                         max_digits=7, decimal_places=2,
                                         validators=[
                                             MaxValueValidator(10000),
                                             MinValueValidator(0),
                                         ]
                                         )

    tags = models.ManyToManyField('Tag', blank=True, default=None, null=True, related_name='project')
    additional_hour_design = models.DecimalField(max_digits=7, decimal_places=2,
                                                 validators=[
                                                     MaxValueValidator(10000),
                                                     MinValueValidator(0),
                                                 ], default=0)
    additional_hour_development = models.DecimalField(max_digits=7,
                                                      decimal_places=2,
                                                      validators=[
                                                          MaxValueValidator(10000),
                                                          MinValueValidator(0),
                                                      ], default=0)
    additional_hour_testing = models.DecimalField(max_digits=7, decimal_places=2,
                                                  validators=[
                                                      MaxValueValidator(10000),
                                                      MinValueValidator(0),
                                                  ], default=0)

    def save(self, *args, **kwargs):
        user = get_request().user
        if self.pk is not None:
            original = Project.objects.get(pk=self.pk)
            if original.actual_testing != self.actual_testing\
                    or original.actual_development != self.actual_development\
                    or original.actual_design != self.actual_design:
                HistoryOfChanges.actual_testing = self.actual_testing
                HistoryOfChanges.actual_development = self.actual_development
                HistoryOfChanges.change_actual_design = self.actual_design
                HistoryOfChanges.objects.get_or_create(
                    change_delta_actual_design=self.actual_design - original.actual_design,
                    resulting_actual_design=self.actual_design,
                    change_delta_actual_development=self.actual_development - original.actual_development,
                    resulting_actual_development=self.actual_development,
                    change_delta_actual_testing=self.actual_testing - original.actual_testing,
                    resulting_actual_testing=self.actual_testing,
                    change_time=timezone.now(),
                    project=original,
                    owner=user
                )
                HistoryOfChanges.save(self, *args, **kwargs)
            # original.actual_design = F('additional_hour_design') + self.actual_design
            # original.refresh_from_db()
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-update', kwargs={'pk': self.pk, 'slug': slugify(self.title)})

    @property
    def has_ended(self):
        return self.end_date is not None and self.end_date < timezone.now().date()

    @property
    def total_estimated_hours(self):
        return self.estimated_design + self.estimated_development + self.estimated_testing

    @property
    def total_actual_hours(self):
        return self.actual_design + self.actual_development +\
               self.actual_testing +\
               self.additional_hour_design +\
               self.additional_hour_development + self.additional_hour_testing

    @property
    def is_over_budget(self):
        return self.total_actual_hours > self.total_estimated_hours


class Tag(models.Model):
    title = models.CharField(max_length=16)

    def get_absolute_url(self):
        return reverse('tag-list')

    def get_update_url(self):
        return reverse('tag-edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('tag-delete', kwargs={'pk': self.id})

    def __str__(self):
        return self.title


class DataOfTag(models.Model):
    tag = models.CharField(max_length=240)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    time_to_add = models.TimeField()

    def __str__(self):
        return f'Tag {self.tag} was attached' \
               f' to a project {self.project.title}, stored.'


class HistoryOfChanges(models.Model):
    change_delta_actual_design = models.CharField(max_length=164, blank=True)
    resulting_actual_design = models.CharField(max_length=164, blank=True)
    change_delta_actual_development = models.CharField(max_length=164, blank=True)
    resulting_actual_development = models.CharField(max_length=164, blank=True)
    change_delta_actual_testing = models.CharField(max_length=164, blank=True)
    resulting_actual_testing = models.CharField(max_length=164, blank=True)
    change_time = models.TimeField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Change in {self.project.title} project at {self.change_time}'


class InitialDataOfProject(models.Model):
    initial_actual_design = models.DecimalField(max_digits=7, decimal_places=2)
    initial_actual_development = models.DecimalField(max_digits=7, decimal_places=2)
    initial_actual_testing = models.DecimalField(max_digits=7, decimal_places=2)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f'Initial data {self.project} project.'