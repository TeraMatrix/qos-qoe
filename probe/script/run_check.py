#! /usr/bin/python
import os,MySQLdb,sys,datetime,time,config
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
# Execute script with host warning critical and timeout parameters
############################################################################################################################
def execute(service):
	start_time=datetime.datetime.now()
	if service['check_name']=="icmp" or service['check_name']=="http" or service['check_name']=="dns":
		command=config.CHECK_PATH+"./check_%s -H %s -w %f -c %f -t %d > "+config.OUTPUT_PATH+"service_%d"
		command%=(service['check_name'],service['host_name'],service['warning'],service['critical'],service['timeout'],service['service_id'])
	elif service['check_name']=="tcp":
		command=config.CHECK_PATH+"./check_%s -H %s -w %f -c %f -t %d -p 80> "+config.OUTPUT_PATH+"service_%d"
		command%=(service['check_name'],service['host_name'],service['warning'],service['critical'],service['timeout'],service['service_id'])
	else:
		command=""
	try:
		return_code=os.system(command)
	except:
		print "\nProcess",os.getpid(),"exiting now..."
		sys.exit()	
	result=get_output(service)
	end_time=datetime.datetime.now()
	#print return_code,result
	save_result(return_code,result,start_time,end_time,service)
############################################################################################################################
# Fetches output from temp file.
############################################################################################################################
def get_output(service):
	out_file=open(config.OUTPUT_PATH+"service_%d"%(service['service_id']))
	out_list=[]
	for line in out_file:
		output=line.split('\n')
		out_list.append(output[0].split('|'))
	result={}
	if len(out_list)==2:
		result['output']=out_list[1][0]
		result['perf_data']=out_list[0][0]
	elif len(out_list)==1:
		if len(out_list[0])==2:
			result['output']=out_list[0][0]
			result['perf_data']=out_list[0][1]
		elif len(out_list[0])==1:
			result['output']=out_list[0][0]
			result['perf_data']=" "		
	return result
############################################################################################################################
# Get current check attempt
############################################################################################################################
def get_current_check_attempt(service,return_code):
	if return_code==0 or return_code==256:
		return 1
	else:
		db=connect_db()
		cursor=db.cursor()
		query="""
				select current_check_attempt from perf_data 
				where start_time=(select max(start_time) from perf_data where service_id=%d) 
				and service_id=%d 
			"""%(service['service_id'],service['service_id'])
		try:
			cursor.execute(query)
			if cursor.rowcount==1:
				result=cursor.fetchone()
				previous_attempt = int(result[0])
				db.close()
				return previous_attempt +1				
			else:
				db.close()
				return 1				
		except:
			db.close()
			return 1
############################################################################################################################
# Saves the result into database.
############################################################################################################################
def save_result(return_code,result,start_time,end_time,service):
	execution_time=float(str(end_time - start_time).split(':')[2])
	current_attempt=get_current_check_attempt(service,return_code)
	if current_attempt<=service['max_attempt']:
		db=connect_db()
		cursor=db.cursor()
		query="""
				insert into perf_data
				(
					service_id, 
					current_check_attempt,
					max_check_attempt,
					start_time,
					end_time,
					timeout,
					execution_time,
					return_code,
					output,
					perfdata,
					check_name,
					check_param,
					target_ip, 
					probe_name
				) values(%d,%d,%d,'%s','%s',%d,%f,%d,'%s','%s','%s','%s','%s','%s')"""
		query%=(service['service_id'],\
				current_attempt,\
				service['max_attempt'],\
				start_time,\
				end_time,\
				service['timeout'],\
				execution_time,\
				return_code,result['output'],\
				result['perf_data'],\
				service['check_name'].upper(),\
				service['check_parameter'],\
				service['host_name'],\
				config.probe_name)
		try:
			cursor.execute(query)
			db.commit()
			db.close()
			return True
		except:
			db.rollback()
			db.close()
			return False
	else:
		return False
############################################################################################################################
# 
############################################################################################################################
