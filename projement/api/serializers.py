from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from projects.models import Project, Company, HistoryOfChanges, \
    InitialDataOfProject


class DashboardListSerializer(ModelSerializer):
    url = serializers.URLField(source='get_api_absolute_url', )
    company = SerializerMethodField()
    estimated = serializers.DecimalField(max_digits=7, decimal_places=2,
                                         source='total_estimated_hours')
    actual = serializers.DecimalField(max_digits=7, decimal_places=2,
                                      source='total_actual_hours')

    class Meta:
        model = Project
        fields = [
            'url',
            'title',
            'company',
            'estimated',
            'actual',
        ]

    def get_company(self, obj):
        return obj.company.name


class CompanyCreateSerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class ProjectUpdateSerializer(ModelSerializer):

    additional_hour_design = serializers.DecimalField(max_digits=7,
                                                      decimal_places=2,
                                                      write_only=True,
                                                      required=False,
                                                      default=0,
                                                      validators=[
                                                          MinValueValidator(0),
                                                          MaxValueValidator(9999)
                                                      ])
    additional_hour_development = serializers.DecimalField(max_digits=7,
                                                           decimal_places=2,
                                                           write_only=True,
                                                           required=False,
                                                           default=0,
                                                           validators=[
                                                               MinValueValidator(0),
                                                               MaxValueValidator(9999)
                                                           ]
                                                           )
    additional_hour_testing = serializers.DecimalField(max_digits=7,
                                                       decimal_places=2,
                                                       write_only=True,
                                                       required=False,
                                                       default=0,
                                                       validators=[
                                                           MinValueValidator(0),
                                                           MaxValueValidator(9999)
                                                       ]
                                                       )

    class Meta:
        model = Project
        fields = [
            'actual_design',
            'actual_development',
            'actual_testing',
            'additional_hour_design',
            'additional_hour_development',
            'additional_hour_testing',
        ]
        read_only_fields = ['actual_design',
                            'actual_development',
                            'actual_testing'
                            ]

    def update(self, instance, validated_data):
        default_value = Decimal(0)
        if Decimal(self.validated_data[
                       'additional_hour_design']) != default_value or \
                Decimal(self.validated_data[
                            'additional_hour_development']) != default_value or \
                Decimal(self.validated_data[
                            'additional_hour_testing']) != default_value:
            HistoryOfChanges.objects.get_or_create(
                change_delta_actual_design=self.validated_data[
                    'additional_hour_design'],
                resulting_actual_design=self.validated_data[
                                            'additional_hour_design'] + self.instance.actual_design,
                change_delta_actual_development=self.validated_data[
                    'additional_hour_development'],
                resulting_actual_development=self.validated_data[
                                                 'additional_hour_development'] + self.instance.actual_development,
                change_delta_actual_testing=self.validated_data[
                    'additional_hour_testing'],
                resulting_actual_testing=self.validated_data[
                                             'additional_hour_testing'] + self.instance.actual_testing,
                change_time=timezone.now(),
                project=self.instance,
                owner=self.context.get('request').user,
            )
        instance.actual_design += Decimal(validated_data.get(
            'additional_hour_design'))
        instance.actual_development += Decimal(validated_data.get(
            'additional_hour_development'))
        instance.actual_testing += Decimal(validated_data.get(
            'additional_hour_testing'))

        instance.save()

        return instance


class ProjectCreateSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

    def save(self, **kwargs):
        project = super(ProjectCreateSerializer, self).save(**kwargs)
        InitialDataOfProject.objects.get_or_create(
            initial_actual_design=self.validated_data.get('actual_design'),
            initial_actual_development=self.validated_data.get('actual_development'),
            initial_actual_testing=self.validated_data.get('actual_testing'),
            project=project
        )
        return project