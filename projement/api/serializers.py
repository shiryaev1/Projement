from decimal import Decimal

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from projects.models import Project


class DashboardListSerializer(ModelSerializer):

    estimated = serializers.DecimalField(max_digits=7, decimal_places=2,
                                         source='total_estimated_hours')
    actual = serializers.DecimalField(max_digits=7, decimal_places=2,
                                      source='total_actual_hours')

    class Meta:
        model = Project
        fields = [
            'title',
            'company',
            'estimated',
            'actual',
        ]


class ProjectUpdateSerializer(ModelSerializer):

    additional_hour_design = serializers.DecimalField(max_digits=7,
                                                      decimal_places=2,
                                                      write_only=True,
                                                      required=False,
                                                      default=0)
    additional_hour_development = serializers.DecimalField(max_digits=7,
                                                           decimal_places=2,
                                                           write_only=True,
                                                           required=False,
                                                           default=0)
    additional_hour_testing = serializers.DecimalField(max_digits=7,
                                                       decimal_places=2,
                                                       write_only=True,
                                                       required=False,
                                                       default=0)

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
        instance.actual_design += Decimal(validated_data.get('additional_hour_design'))
        instance.actual_development += Decimal(validated_data.get('additional_hour_development'))
        instance.actual_testing += Decimal(validated_data.get('additional_hour_testing'))

        instance.save()

        return instance
