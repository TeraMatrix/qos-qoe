#! /usr/bin/python
import os,MySQLdb,time,sys,run_check,run_health,aggregator,config
from multiprocessing import Process
############################################################################################################################
# Connect to database.
############################################################################################################################
def connect_db():
	try:
		return MySQLdb.connect(config.probe_server,config.username,config.password,config.dbname)
	except:
		print "DB connection error"
		sys.exit()
############################################################################################################################
# Get configuration lock status
############################################################################################################################
def get_conf_lock():
	db=connect_db()
	cursor=db.cursor()
	query="select status from probe_lock where name='conf_update'"
	try:
		cursor.execute(query)
		result=cursor.fetchone()
		status = result[0]
		#print status
		if status=='0':
			db.close()
			return True
		else:
			db.close()
			return False
	except:
		db.close()
		return False
############################################################################################################################
# Update configuration lock status
############################################################################################################################
def update_conf_lock():
	db=connect_db()
	cursor=db.cursor()
	query="update probe_lock set status=0 where name='conf_update'"
	try:
		cursor.execute(query)
		db.commit()
		db.close()
		return True
	except:
		db.rollback()
		db.close()
		return False
############################################################################################################################
# Get configuration
############################################################################################################################
def get_conf():
	db=connect_db()
	if get_conf_lock():
		cursor=db.cursor()
		query="select * from Nocout_Probe_Service_Conf"
		try:
			cursor.execute(query)
			services=cursor.fetchall()
			db.close()
			return services
		except:
			print "Error in fetching configuration"
			db.close()
			return get_conf()
	else:
		while not update_conf_lock():
			print "Updating configuration..."
		db.close()
		return get_conf()
############################################################################################################################
# Start a parallel process of service check
############################################################################################################################
def start_checks_processes(services):
	services=get_conf()
	process_list={}
	for row in services:
		service_details={}
		service_details['service_id']=int(row[0])
		service_details['check_name']=row[1].lower()
		service_details['check_parameter']=row[2]
		service_details['host_name']=row[3]
		service_details['warning']=float(row[4])
		service_details['critical']=float(row[5])
		service_details['timeout']=int(row[6])
		service_details['max_attempt']=int(row[7])
		service_details['check_interval']=int(row[8])
		process_list[service_details['service_id']]=Process(target=run_checks,args=(service_details,))
		process_list[service_details['service_id']].start()
	return process_list
############################################################################################################################
# Run the check command in interval
############################################################################################################################
def run_checks(service_details):
	while get_conf_lock():
		print "Service id", service_details['service_id'],"is executing"
		try:
			run_check.execute(service_details)
		except:
			sys.exit()
		sleep(service_details['check_interval'])
	print "Check with service id", service_details['service_id'],"found update in configuration. Exiting now.."
	return
############################################################################################################################
# Run the health service in interval
############################################################################################################################
def run_health_service(interval):
	while get_conf_lock():
		print "Health service is executing"
		try:
			run_health.execute()
		except:
			sys.exit()
		sleep(interval)
	print "Health service found update in configuration. Exiting now.."
	return
############################################################################################################################
# Run the aggregator in interval
############################################################################################################################
def run_aggregator(interval):
	while get_conf_lock():
		print "Aggregator executing"
		try:
			aggregator.read_From_Db()
		except:
			sys.exit()
		sleep(interval)
	print "Aggregator found update in configuration. Exiting now.."
	return
############################################################################################################################
# Terminate checks processes
############################################################################################################################
def terminate_checks(process_list):
	for service_id in process_list:
		if process_list[service_id].is_alive():
			print "Terminating service",service_id
			process_list[service_id].terminate()
		else:
			print "Service",service_id,"has already exited"
############################################################################################################################
# Sleeps and waits until a interupt occurs
############################################################################################################################
def sleep(minutes):
	try:
		time.sleep(minutes*60)
	except:
		print "\nProcess",os.getpid(),"exiting now..."
		sys.exit();	
def sleep_loop(minutes,process_list):
	try:
		time.sleep(minutes*60)
	except:
		terminate_checks(process_list)
		print "\nProcess",os.getpid(),"exiting now..."
		sys.exit();	
############################################################################################################################
# Main function
############################################################################################################################
if __name__ == "__main__":
	interval=1
	print "Starting monitoring"
	if not get_conf_lock():
		print "Updating configuration"
		while not update_conf_lock():
			print "Error in updating configuration"
	while True:
		services=get_conf()
		process_list=start_checks_processes(services)
		process_list['health_process']=Process(target=run_health_service,args=(interval,))
		process_list['health_process'].start()
		process_list['aggregator_process']=Process(target=run_aggregator,args=(interval,))
		process_list['aggregator_process'].start()
		while get_conf_lock():
			print "No configuration changes. All services running."
			sleep_loop(interval,process_list)		
		print "Configuration changed"
		print "Termiating all check processes"
		terminate_checks(process_list)
		print "Updating configuration and lock"
		while not update_conf_lock():
			print "Updating..."
		print "Restarting monitoring"
############################################################################################################################
# 
############################################################################################################################
