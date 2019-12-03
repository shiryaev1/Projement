import uuid

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator


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

    tags = models.ForeignKey('Tag', blank=True, default=None, null=True,
                             on_delete=models.CASCADE)
    additional_hour_design = models.DecimalField(max_digits=7, decimal_places=2,
                                            validators=[
                                                MaxValueValidator(10000),
                                                MinValueValidator(0),
                                            ], default=0)
    additional_hour_development = models.DecimalField(max_digits=7, decimal_places=2,
                                            validators=[
                                                MaxValueValidator(10000),
                                                MinValueValidator(0),
                                            ], default=0)
    additional_hour_testing = models.DecimalField(max_digits=7, decimal_places=2,
                                            validators=[
                                                MaxValueValidator(10000),
                                                MinValueValidator(0),
                                            ], default=0)

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
               self.actual_testing + self.additional_hour_design +\
               self.additional_hour_development + self.additional_hour_testing

    @property
    def is_over_budget(self):
        return self.total_actual_hours > self.total_estimated_hours


class Tag(models.Model):
    title = models.CharField(max_length=16)

    def get_update_url(self):
        return reverse('tag-edit', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('tag-delete', kwargs={'id': self.id})

    def __str__(self):
        return self.title


class DataOfTag(models.Model):
    tag = models.CharField(max_length=240)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    time_to_add = models.TimeField()

    def __str__(self):
        return f'Tag {self.tag} was attached' \
               f' to a project {self.project.title}, stored.'