from django.shortcuts import render

# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import *
from Nocout.models import *

from datetime import datetime
import calendar
from json import dumps
import json
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

	return render_to_response('Nocout/probes.html',probe_details,context)

def service_selection(probe_id,SVC_Name):
	if SVC_Name == "HTTP_Browsing":
		services = Probe_Service_Conf.objects.raw('SELECT * FROM Nocout_probe_service_conf WHERE SVC_NAME="HTTP" AND SVC_Param="Response Time" AND Probe_ID_id=%s',[probe_id])
	elif SVC_Name == "Downlink":
		services = Probe_Service_Conf.objects.raw('SELECT * FROM Nocout_probe_service_conf WHERE SVC_NAME="HTTP" AND SVC_Param="Downlink" AND Probe_ID_id=%s',[probe_id])
	else:
		services = Probe_Service_Conf.objects.filter(Probe_ID_id=probe_id,SVC_Name=SVC_Name)
	return services


##################################################################################
# RETRIEVE THE SELECTED PROBE AND SERVICES DETAILS 
##################################################################################
def Probe_details(request):
	print "Hello"
	if request.method == 'GET': 

		# TO GET THE DETAILS OF THE SELECTED PROBE
		probe_id = request.GET.get('Probe_ID')
		print "ptrtrtr:" ,probe_id
		detail = Probe_Details.objects.filter(Probe_ID=probe_id)
		probe_details['detail']=detail
		probe_details['probe_id'] = probe_id;
		# END OF PROBE DETAILS
		
		# TO GET THE SERVICES DETAILS
		probe_details['Service_HTTP_Throughput'] = service_selection(probe_id,"Downlink")
		probe_details['Service_ICMP'] = service_selection(probe_id,"ICMP")
		probe_details['Service_TCP'] = service_selection(probe_id,"TCP")
		probe_details['Service_DNS'] = service_selection(probe_id,"DNS")
		probe_details['Service_HTTP_Browsing'] = service_selection(probe_id,"HTTP_Browsing")

		# END OF TO GET THE SERVICES DETAILS

		return redirect('probes.html',probe_details)


def Probe_services_details(request):
	print "IN the services details"
	probe_id = probe_details['probe_id']
	probe_details['services_cor_probe'] = probe_id
	if request.method == 'GET': 
		# TO GET THE DETAILS OF THE HTTP_DOWNLINK
	
		service_HTTP_throughput = request.GET.get('HTTP_Throughput')
		if service_HTTP_throughput != None:
			probe_details['service_HTTP_throughput'] = int(service_HTTP_throughput)
		
		performance_HTTP_Downlink = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE Service_ID_id=%s ORDER BY TimeStamp DESC LIMIT 10',[service_HTTP_throughput])
		# performance_HTTP_Downlink = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE SVC_Name="HTTP" AND SVC_Param = "Downlink" AND Probe_ID_id= %s ORDER BY TimeStamp DESC LIMIT 10',[probe_id])

		probe_details['performance_HTTP_Downlink'] = performance_HTTP_Downlink
		performance_HTTP_Downlink = []
	
		for value in probe_details['performance_HTTP_Downlink']:
			time = str(value.TimeStamp)
			performance_HTTP_Downlink.append([time,float(value.Value)])
	
		for data in range(len(performance_HTTP_Downlink)):
			performance_HTTP_Downlink[data][0] = datetime.strptime(performance_HTTP_Downlink[data][0][:19],'%Y-%m-%d %H:%M:%S')
			performance_HTTP_Downlink[data][0] = calendar.timegm(performance_HTTP_Downlink[data][0].timetuple())
			
		# SERIALIZE INTO JSON FOR USE IN JAVASCRIPT
		performance_HTTP_Downlink = simplejson.dumps(performance_HTTP_Downlink)

		probe_details['HTTP_Downlink'] = performance_HTTP_Downlink
		# END OF HTTP_DOWNLINK 

		# TO GET THE DETAILS OF THE ICMP_Avg_RTA
		service_ICMP = request.GET.get('ICMP')
		if service_ICMP != None:
			probe_details['service_ICMP'] = int(service_ICMP)

		performance_ICMP_Avg_RTA = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE Service_ID_id=%s AND SVC_Param = "Avg. RTA" ORDER BY TimeStamp DESC LIMIT 10',[service_ICMP])
		
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
		performance_ICMP_Pkt_LOSS = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE Service_ID_id=%s AND SVC_Param = "Packet Loss" ORDER BY TimeStamp DESC LIMIT 10',[service_ICMP])

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
		service_TCP_Response_Time = request.GET.get('TCP')
		print service_TCP_Response_Time
		if service_TCP_Response_Time != None:
			probe_details['service_TCP_Response_Time'] = int(service_TCP_Response_Time)

		performance_TCP_Response_Time = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE Service_ID_id=%s ORDER BY TimeStamp DESC LIMIT 10',[service_TCP_Response_Time])

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
		service_DNS_Response_Time = request.GET.get('DNS')
		print service_DNS_Response_Time
		if service_DNS_Response_Time != None:
			probe_details['service_DNS_Response_Time'] = int(service_DNS_Response_Time)

		performance_DNS_Response_Time = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE Service_ID_id=%s ORDER BY TimeStamp DESC LIMIT 10',[service_DNS_Response_Time])

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

	# TO GET THE DETAILS OF THE HTTP_DOWNLINK
		service_HTTP_Browsing = request.GET.get('HTTP_Browsing')
		if service_HTTP_Browsing != None:
			probe_details['service_HTTP_Browsing'] = int(service_HTTP_Browsing)
		
		performance_HTTP_Browsing = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE Service_ID_id=%s ORDER BY TimeStamp DESC LIMIT 10',[service_HTTP_Browsing])
		# performance_HTTP_Downlink = Performance_Services.objects.raw('SELECT * FROM Nocout_performance_services WHERE SVC_Name="HTTP" AND SVC_Param = "Downlink" AND Probe_ID_id= %s ORDER BY TimeStamp DESC LIMIT 10',[probe_id])

		probe_details['performance_HTTP_Browsing'] = performance_HTTP_Browsing
		performance_HTTP_Browsing = []
	
		for value in probe_details['performance_HTTP_Browsing']:
			time = str(value.TimeStamp)
			performance_HTTP_Browsing.append([time,float(value.Value)])
	
		for data in range(len(performance_HTTP_Browsing)):
			performance_HTTP_Browsing[data][0] = datetime.strptime(performance_HTTP_Browsing[data][0][:19],'%Y-%m-%d %H:%M:%S')
			performance_HTTP_Browsing[data][0] = calendar.timegm(performance_HTTP_Browsing[data][0].timetuple())
			
		# SERIALIZE INTO JSON FOR USE IN JAVASCRIPT
		performance_HTTP_Browsing = simplejson.dumps(performance_HTTP_Browsing)

		probe_details['HTTP_Browsing'] = performance_HTTP_Browsing
		# END OF HTTP_DOWNLINK 

		
		return redirect('probes.html',probe_details)

def Inventory(request):
	context = RequestContext(request)
	
	
	return render_to_response('Nocout/inventory.html',probe_details,context)
			


def registration(request):
	context=RequestContext(request)

	if request.method =='GET':
		return render_to_response('Nocout/registration.html',context)

	if request.method =='POST':
		Probe_Name=str(request.POST.get('Probe_Name'))
		
		Latitute = request.POST.get('Latitude')
		Longitude = request.POST.get('Longtitute')
		Probe_IP_Address = str(request.POST.get('Probe IP Address'))
		Probe_Auth_Mechan = str(request.POST.get('Probe_Authentication_Mechanism'))
		Probe_Speed = str(request.POST.get('Probe Speed'))
		Version = str(request.POST.get('Version'))
		MAC_Address = str(request.POST.get('MAC Address'))
		Connected_To=str(request.POST.get('Connected To'))
		Central_Server_IP=str(request.POST.get('Central Server IP'))

		result = Probe_ID_Name.objects.create(Probe_Name=Probe_Name)
		probe_id =  int(result.Probe_ID)

		connected_ID = Probe_Connection.objects.filter(Connection_To = Connected_To)
		for value in connected_ID:
			connected_ID = int(value.Connection)

		try:
			details = Probe_Details.objects.create(Probe_ID_id= probe_id,Latitute=Latitute,Longtitute=Longitude,Probe_Name=Probe_Name,Probe_IP_Address=Probe_IP_Address,Probe_Auth_Mechan=Probe_Auth_Mechan,Probe_Speed=Probe_Speed,Version=Version,Mac_Address=MAC_Address,Central_Server_IP=Central_Server_IP,Connected_To=connected_ID)
			print details
		
			return redirect('index.html')
		except:
			return redirect('registration.html')


		
	



	

