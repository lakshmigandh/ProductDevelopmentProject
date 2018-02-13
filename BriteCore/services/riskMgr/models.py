


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


#Metadata table to specify the supported number of datatypes for fields.
class FieldTypes(models.Model):
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=50)

#Metadata table to specify the supported number of custom constraints/validations for fields.
class FieldConstraintTypes(models.Model):
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

#Models custom risk entities created by different clients/corporations
class RiskEntityTypes(models.Model):
    entityTypeId = models.AutoField(primary_key=True)
    clientId = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    noOfUDFS = models.IntegerField()

#Models primary data of custom risk entities
class RiskEntityDataMappings(models.Model):
    dataMappingId = models.AutoField(primary_key=True)
    entityTypeId = models.ForeignKey('RiskEntityTypes')
    entityDataId = models.IntegerField()

#Models custom fields of custom risk entities
class RiskEntityTypeFields(models.Model):
    fieldId = models.AutoField(primary_key=True)
    entityTypeId = models.ForeignKey(RiskEntityTypes,related_name='riskentitytypefields')
    type = models.ForeignKey('FieldTypes')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

#Models custom constraints/validations for custom fields of custom risk entities
class RiskEntityFieldConstraints(models.Model):
    constraintId = models.AutoField(primary_key=True)
    type = models.ForeignKey('FieldConstraintTypes')
    fieldId = models.ForeignKey('RiskEntityTypeFields',related_name='riskentityfieldconstraints')
    value = models.CharField(max_length=500)

#Models actual data for custom fields of custom risk entities
class RiskEntityCharFieldValues(models.Model):
    fieldDataId = models.AutoField(primary_key=True)
    entityDataId = models.ForeignKey('RiskEntityDataMappings')
    fieldId = models.ForeignKey('RiskEntityTypeFields')
    value = models.CharField(max_length=500)

class RiskEntityIntFieldValues(models.Model):
    fieldDataId = models.AutoField(primary_key=True)
    entityDataId = models.ForeignKey('RiskEntityDataMappings')
    fieldId = models.ForeignKey('RiskEntityTypeFields')
    value = models.IntegerField()

class RiskEntityDateFieldValues(models.Model):
    fieldDataId = models.AutoField(primary_key=True)
    entityDataId = models.ForeignKey('RiskEntityDataMappings')
    fieldId = models.ForeignKey('RiskEntityTypeFields')
    value = models.DateTimeField()
