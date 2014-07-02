''' Django View class which handles all the request of the API
Made using Django Rest Framework.
For more info : http://www.django-rest-framework.org/
'''

from Nocout.models import Probe_ID_Name
from api.serializer import ProbeSerializer
from Nocout.models import Probe_Service_Conf
from api.serializer import ConfigSerializer
from Nocout.models import Health_Service 
from api.serializer import HealthSerializer
from Nocout.models import Performance_Services
from api.serializer import PerformanceSerializer
from rest_framework import generics
# Create your views here.

class ProbeList(generics.ListAPIView):
	'''View class for getting Probe_ID in response to Probe Name'''

	serializer_class=ProbeSerializer
	def get_queryset(self):
		queryset=Probe_ID_Name.objects.all()
		ID=self.request.QUERY_PARAMS.get('Probe_Name',None)
		if ID is not None:
			queryset=queryset.filter(Probe_Name=ID)
		return queryset

class ConfigDetails(generics.ListCreateAPIView):
	'''View Class to get the Configuration Details from Central server by Probes'''
	serializer_class = ConfigSerializer
	def get_queryset(self):
		queryset=Probe_Service_Conf.objects.all()
		Probe_Detail=self.request.QUERY_PARAMS.get('Probe_ID',None)
		if Probe_Detail is not None:
			queryset=queryset.filter(Probe_ID=Probe_Detail)
		return queryset

class HealthDetails(generics.CreateAPIView):
	'''View class used for posting Health Details to Central Server from Probe'''
	queryset=Health_Service.objects.all()
	serializer_class = HealthSerializer

class PerformanceDetails(generics.CreateAPIView):
	'''View class used for posting performance to Central Server from Probe'''
	queryset=Performance_Services.objects.all()
	serializer_class = PerformanceSerializer


