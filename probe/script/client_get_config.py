#!/usr/bin/env python
import MySQLdb, requests, config, json, sys, config

#### Request Configuraion from Central Server#####

def getProbe_id():
	db=MySQLdb.connect(config.probe_server,config.username,config.password,config.dbname)
	cursor=db.cursor(MySQLdb.cursors.DictCursor);
	query="SELECT * from probe_lock where name='Probe_id'"
	try:
		cursor.execute(query)
		result=cursor.fetchall();
		db.commit()
		db.close()
		return result[0]['status']
	except:
		db.close()
		print "ERROR"
		return -1


def getConfiguration():
	st="configuration?Probe_ID="
	if getProbe_id()==-1:
		print "Probe ID not present in database."
		print "Exiting Now."
		sys.exit()
	query=config.central_server+st+str(getProbe_id())
	try:
		data=json.loads((requests.get(query)).text);
	except:
		print sys.exc_info()[0]
		print "Exception in Connection and request library..."
		return -1;
	####Connecting to the databases##################
	db=MySQLdb.connect(config.probe_server,config.username,config.password,config.dbname)
	################################################
	cursor=db.cursor()
	
	########Updating Lock in the Database###########
	def update_conf_lock():
		query="update probe_lock set status=1 where name='conf_update'"
		try:
			cursor.execute(query)
			db.commit()
			return True
		except:
			db.rollback()
			return False
	###########Extracting Configuration data########
	for instance in data:
		'''Etraction of data to be pushed into Probe_Configuration'''
		service_id=instance["id"]
		check_name=str(instance["SVC_Name"])
		check_parameter=str(instance["SVC_Param"])
		ip_host_address=str(instance["Target_IP"])
		warning=float(instance["Warn_Thresh"])
		critical=float(instance["Criti_THresh"])
		timeout=int(instance["Timeout_Thresh"])
		max_attempt=int(instance["Max_Attempt"])
		check_interval=int(instance["Interval"])
		'''Preparing Queury'''
		sql="""INSERT INTO Nocout_Probe_Service_Conf(service_id,check_name,check_parameter,ip_host_address,warning,critical,timeout,max_attempt,check_interval) values(%d,'%s','%s','%s',%f,%f,%d,%d,%d)"""
		sql%=(service_id,check_name,check_parameter,ip_host_address,warning,critical,timeout,max_attempt,check_interval)

		try:
			cursor.execute(sql)
			db.commit()
			if update_conf_lock()==True:
				print "Configuration Lock updated"
			else:
				print "Error in updating lock from central server..."
			return 1
		except:
			db.rollback()
			print sys.exc_info()
			return -1
		#################################################
	db.close()

	
