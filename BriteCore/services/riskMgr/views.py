


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template import Context, loader
from django.http import HttpResponse
from rest_framework import serializers
from .models import *
from .serializers import RiskEntityTypesSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class RiskMgr(APIView):
    def get(self, request, format=None,risktype=None):
	print "RiskType is "+risktype
	if not risktype:
		rets = RiskEntityTypes.objects.filter(clientId=1).prefetch_related('riskentitytypefields__riskentityfieldconstraints')
		data = JSONResponse(RiskEntityTypesSerializer(rets,many=True).data)
	else:
		rets = RiskEntityTypes.objects.filter(clientId=1,name=risktype).prefetch_related('riskentitytypefields__riskentityfieldconstraints')
		data = JSONResponse(RiskEntityTypesSerializer(rets,many=True).data)
	print data
	return data

def index(request,risktype=None):
    print risktype
    template = loader.get_template("pages/index.html")
    return render(request,"pages/index.html",{'model':risktype})


def refreshMetaData(request):
    RiskEntityCharFieldValues.objects.all().delete()
    RiskEntityIntFieldValues.objects.all().delete()
    RiskEntityDateFieldValues.objects.all().delete()
    RiskEntityFieldConstraints.objects.all().delete()
    RiskEntityTypeFields.objects.all().delete()
    RiskEntityDataMappings.objects.all().delete()
    RiskEntityTypes.objects.all().delete()
    FieldConstraintTypes.objects.all().delete()
    FieldTypes.objects.all().delete()

    #FieldTypes MetaData
    textType = FieldTypes.objects.create(type="text",description="Text Field")
    numberType = FieldTypes.objects.create(type="number",description="Number Field")
    dateType = FieldTypes.objects.create(type="date",description="Date Field")
    #Constraints MetaData
    anyOfConstraint = FieldConstraintTypes.objects.create(type="ANY_OF",description="Allow only set of values")
    maxValConstraint = FieldConstraintTypes.objects.create(type="MAX_VALUE",description="Max Value validation")
    minValConstraint = FieldConstraintTypes.objects.create(type="MIN_VALUE",description="Min Value validation")
    maxLenConstraint = FieldConstraintTypes.objects.create(type="MAX_LENGTH",description="Max Length validation")
    reqConstraint = FieldConstraintTypes.objects.create(type="REQUIRED",description="Required field validation")
    emailConstraint = FieldConstraintTypes.objects.create(type="EMAIL",description="Email Field validation")
    passwordConstraint = FieldConstraintTypes.objects.create(type="PASSWORD",description="Password field validation")

    #Custom models are defined here. Once endpoints/UI are done, these can even be got from user input

    #Prize Model
    prizeModel = RiskEntityTypes.objects.create(clientId=1,name="Prize",description="Prize Model",noOfUDFS=4)
    prizeName = RiskEntityTypeFields.objects.create(entityTypeId=prizeModel,type=textType,name="Prize Name",description="Name of the Prize Insured")
    prizeDate = RiskEntityTypeFields.objects.create(entityTypeId=prizeModel,type=dateType,name="Prize Date",description="Prize Insured Date")
    prizeAmount = RiskEntityTypeFields.objects.create(entityTypeId=prizeModel,type=numberType,name="Prize Amount",description="Prize Amount Insured")
    insuranceType = RiskEntityTypeFields.objects.create(entityTypeId=prizeModel,type=textType,name="Type of insurance",description="Type of insurance")
    RiskEntityFieldConstraints.objects.create(type=reqConstraint,fieldId=prizeName,value="Y")
    RiskEntityFieldConstraints.objects.create(type=reqConstraint,fieldId=prizeDate,value="Y")
    RiskEntityFieldConstraints.objects.create(type=reqConstraint,fieldId=prizeAmount,value="Y")
    RiskEntityFieldConstraints.objects.create(type=reqConstraint,fieldId=insuranceType,value="Y")
    RiskEntityFieldConstraints.objects.create(type=anyOfConstraint,fieldId=insuranceType,value="Self")
    RiskEntityFieldConstraints.objects.create(type=anyOfConstraint,fieldId=insuranceType,value="Spouse")
    RiskEntityFieldConstraints.objects.create(type=anyOfConstraint,fieldId=insuranceType,value="Children")


    #Vehicle Model
    vehicleModel = RiskEntityTypes.objects.create(clientId=1,name="Vehicle",description="Vehicle Model",noOfUDFS=4)
    vehicleBrandInsName = RiskEntityTypeFields.objects.create(entityTypeId=vehicleModel,type=textType,name="Insurer's Name",description="Name of the Insurer")
    vehicleBrandInsAge = RiskEntityTypeFields.objects.create(entityTypeId=vehicleModel,type=numberType,name="Age",description="Age of the Insurer")
    vehicleBrandInsEmail = RiskEntityTypeFields.objects.create(entityTypeId=vehicleModel,type=textType,name="E-Mail",description="E-Mail of the Insurer")
    vehicleBrand = RiskEntityTypeFields.objects.create(entityTypeId=vehicleModel,type=textType,name="Brand",description="Name of the Brand")
    vehiclePurchaseDate = RiskEntityTypeFields.objects.create(entityTypeId=vehicleModel,type=dateType,name="Purchase Date",description="Purchase date of the vehicle")
    vehicleClaimAmount = RiskEntityTypeFields.objects.create(entityTypeId=vehicleModel,type=numberType,name="Claim Amount",description="Claim Amount")
    
    RiskEntityFieldConstraints.objects.create(type=reqConstraint,fieldId=vehicleBrand,value="Y")
    RiskEntityFieldConstraints.objects.create(type=reqConstraint,fieldId=vehicleBrandInsName,value="Y")
    RiskEntityFieldConstraints.objects.create(type=reqConstraint,fieldId=vehicleBrandInsAge,value="Y")
    RiskEntityFieldConstraints.objects.create(type=minValConstraint,fieldId=vehicleBrandInsAge,value="18")
    RiskEntityFieldConstraints.objects.create(type=maxValConstraint,fieldId=vehicleBrandInsAge,value="55")
    RiskEntityFieldConstraints.objects.create(type=reqConstraint,fieldId=vehicleBrandInsEmail,value="Y")
    RiskEntityFieldConstraints.objects.create(type=emailConstraint,fieldId=vehicleBrandInsEmail,value="Y")
    RiskEntityFieldConstraints.objects.create(type=reqConstraint,fieldId=vehiclePurchaseDate,value="Y")
    RiskEntityFieldConstraints.objects.create(type=reqConstraint,fieldId=vehicleClaimAmount,value="Y")


    return HttpResponse("MetaData refreshed")
