from django.shortcuts import render

# Create your views here.

# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import *
from Nocout.models import *

from django.utils import simplejson

probe_details = {}

def index(request):
	context = RequestContext(request)
	z1 = 50
	timestamp_dict = {'val':z1}

	return render_to_response('Nocout/index.html',timestamp_dict,context)

##################################################################################
# RETRIEVE THE NAME OF THE REGISTERED PROBES
##################################################################################
def probes(request):
	context = RequestContext(request)

	id_name = Probe_ID_Name.objects.raw('SELECT * FROM Nocout_probe_id_name INNER JOIN Nocout_registered_probes on Nocout_registered_probes.Probe_ID_id = Nocout_probe_id_name.Probe_ID')
	
	probe_details['reg_probe']=id_name
	
	print "Probe"
	print probe_details

	return render_to_response('Nocout/probes.html',probe_details,context)

##################################################################################
# RETRIEVE THE SELECTED PROBE AND SERVICES DETAILS 
##################################################################################
def Probe_details(request):
	print "Hello"
	if request.method == 'GET': 


		# TO GET THE DETAILS OF THE SELECTED PROBE
		probe_id = request.GET.get('Probe_ID')
		detail = Probe_Details.objects.filter(Probe_ID=probe_id)
		probe_details['detail']=detail
		# END OF PROBE DETAILS



		# TO GET THE DETAILS OF THE HTTP_DOWNLINK
		performance_HTTP_Downlink = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE SVC_Name="HTTP" AND SVC_Param = "Downlink" AND Probe_ID_id= %s ORDER BY TimeStamp DESC LIMIT 10',[probe_id])

		probe_details['performance_HTTP_Downlink'] = performance_HTTP_Downlink
		performance_HTTP_Downlink = []
	
		for value in probe_details['performance_HTTP_Downlink']:
			performance_HTTP_Downlink.append(float(value.Value))
	
		print performance_HTTP_Downlink
		# SERIALIZE INTO JSON FOR USE IN JAVASCRIPT
		import json
		performance_HTTP_Downlink = simplejson.dumps(performance_HTTP_Downlink)

		probe_details['HTTP_Downlink'] = performance_HTTP_Downlink
		# END OF HTTP_DOWNLINK 




		# TO GET THE DETAILS OF THE HTTP_UPLINK
		performance_HTTP_Uplink = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE SVC_Name="HTTP" AND SVC_Param = "Uplink" AND Probe_ID_id= %s ORDER BY TimeStamp DESC LIMIT 10',[probe_id])

		probe_details['performance_HTTP_Uplink'] = performance_HTTP_Uplink
		performance_HTTP_Uplink = []
	
		for value in probe_details['performance_HTTP_Uplink']:
			performance_HTTP_Uplink.append(float(value.Value))
	
		performance_HTTP_Uplink = simplejson.dumps(performance_HTTP_Uplink)
		
		probe_details['HTTP_Uplink'] = performance_HTTP_Uplink
		# END OF HTTP_UPLINK



		# TO GET THE DETAILS OF THE ICMP_Avg_RTA
		performance_ICMP_Avg_RTA = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE SVC_Name="ICMP" AND SVC_Param = "Avg. RTA" AND Probe_ID_id= %s ORDER BY TimeStamp DESC LIMIT 10',[probe_id])

		probe_details['performance_ICMP_Avg_RTA'] = performance_ICMP_Avg_RTA
		performance_ICMP_Avg_RTA = []
	
		for value in probe_details['performance_ICMP_Avg_RTA']:
			performance_ICMP_Avg_RTA.append(float(value.Value))
	
	
		# SERIALIZE INTO JSON FOR USE IN JAVASCRIPT
		import json
		performance_ICMP_Avg_RTA = simplejson.dumps(performance_ICMP_Avg_RTA)

		probe_details['ICMP_Avg_RTA'] = performance_ICMP_Avg_RTA
		# END OF ICMP_Avg_RTA



		# TO GET THE DETAILS OF THE ICMP_PKT_LOSS
		performance_ICMP_Pkt_LOSS = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE SVC_Name="ICMP" AND SVC_Param = "Packet Loss" AND Probe_ID_id= %s ORDER BY TimeStamp DESC LIMIT 10',[probe_id])

		probe_details['performance_ICMP_Pkt_LOSS'] = performance_ICMP_Pkt_LOSS
		performance_ICMP_Pkt_LOSS = []
	
		for value in probe_details['performance_ICMP_Pkt_LOSS']:
			performance_ICMP_Pkt_LOSS.append(float(value.Value))
	
	
		# SERIALIZE INTO JSON FOR USE IN JAVASCRIPT
		import json
		performance_ICMP_Pkt_LOSS = simplejson.dumps(performance_ICMP_Pkt_LOSS)

		probe_details['ICMP_Pkt_LOSS'] = performance_ICMP_Pkt_LOSS
		# END OF ICMP_Pkt_LOSS


		# TO GET THE DETAILS OF THE TCP_Response_Time
		performance_TCP_Response_Time = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE SVC_Name="TCP" AND SVC_Param = "Response Time" AND Probe_ID_id= %s ORDER BY TimeStamp DESC LIMIT 10',[probe_id])

		probe_details['performance_TCP_Response_Time'] = performance_TCP_Response_Time
		performance_TCP_Response_Time = []
	
		for value in probe_details['performance_TCP_Response_Time']:
			performance_TCP_Response_Time.append(float(value.Value))
	
	
		# SERIALIZE INTO JSON FOR USE IN JAVASCRIPT
		import json
		performance_TCP_Response_Time = simplejson.dumps(performance_TCP_Response_Time)

		probe_details['TCP_Response_Time'] = performance_TCP_Response_Time
		# END OF TCP_Response_Time



		# TO GET THE DETAILS OF THE DNS_Response_Time
		performance_DNS_Response_Time = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE SVC_Name="DNS" AND SVC_Param = "Response Time" AND Probe_ID_id= %s ORDER BY TimeStamp DESC LIMIT 10',[probe_id])

		probe_details['performance_DNS_Response_Time'] = performance_DNS_Response_Time
		performance_DNS_Response_Time = []
	
		for value in probe_details['performance_DNS_Response_Time']:
			performance_DNS_Response_Time.append(float(value.Value))
	
	
		# SERIALIZE INTO JSON FOR USE IN JAVASCRIPT
		import json
		performance_DNS_Response_Time = simplejson.dumps(performance_DNS_Response_Time)

		probe_details['DNS_Response_Time'] = performance_DNS_Response_Time
		# END OF DNS_Response_Time



		# TO GET THE DETAILS OF THE HEALTH
		performance_HEALTH = Performance_Services.objects.raw('SELECT * FROM Nocout_health_service WHERE Probe_ID_id= %s ORDER BY TimeStamp DESC LIMIT 10',[probe_id])

		probe_details['performance_HEALTH'] = performance_HEALTH
		performance_Health_CPU_Usage = []
		performance_Health_Latency = []

		for value in probe_details['performance_HEALTH']:
			performance_Health_CPU_Usage.append(float(value.CPU_Usage))
			performance_Health_Latency.append(float(value.Latency))
	
		# SERIALIZE INTO JSON FOR USE IN JAVASCRIPT
		import json
		performance_Health_CPU_Usage = simplejson.dumps(performance_Health_CPU_Usage)
		performance_Health_Latency = simplejson.dumps(performance_Health_Latency)

		probe_details['Health_CPU_Usage'] = performance_Health_CPU_Usage
		probe_details['Health_Latency'] = performance_Health_Latency
		# END OF HEALTH

		print probe_details['Health_Latency']
		print probe_details['Health_CPU_Usage']
		return redirect('probes.html',probe_details)


