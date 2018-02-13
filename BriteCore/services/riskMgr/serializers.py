
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers
from .models import *

class FieldTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldTypes
        fields = ('type','description')

class FieldConstraintTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldConstraintTypes
        fields = ('type','description')


class RiskEntityFieldConstraintsSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="type.type", read_only=True)

    class Meta:
        model = RiskEntityFieldConstraints
        fields = ('type','value')


class RiskEntityTypeFieldsSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="type.type", read_only=True)
    constraints = RiskEntityFieldConstraintsSerializer(source="riskentityfieldconstraints", read_only=True, many=True)	

    class Meta:
        model = RiskEntityTypeFields
        fields = ('type','name', 'description','constraints')


class RiskEntityTypesSerializer(serializers.ModelSerializer):

    fields = RiskEntityTypeFieldsSerializer(source="riskentitytypefields", read_only=True, many=True)	

    class Meta:
        model = RiskEntityTypes
        fields = ('entityTypeId','name', 'description','fields')


