'''Serializer for serializing the data used 
Rest framework Serializer class.
To have brevity used ModelSerializer'''

from django.forms import widgets
from rest_framework import serializers
from Nocout.models import Probe_Service_Conf
from Nocout.models import Health_Service
from Nocout.models import Performance_Services
from Nocout.models import Probe_ID_Name
 
class ProbeSerializer(serializers.ModelSerializer):
	class Meta:
		model=Probe_ID_Name
class ConfigSerializer(serializers.ModelSerializer):
	class Meta:
		model=Probe_Service_Conf
class HealthSerializer(serializers.ModelSerializer):
	class Meta:
		model=Health_Service
class PerformanceSerializer(serializers.ModelSerializer):
	class Meta:
		model=Performance_Services
