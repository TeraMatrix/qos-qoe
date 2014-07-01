#! /usr/bin/python
import os,MySQLdb,sys,datetime,time,re,config
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
def execute():
	start_time=datetime.datetime.now()
	check_cpu=config.CHECK_PATH+"./check_cpu -w %d -c %d > "%(config.cpu_w,config.cpu_c)+config.OUTPUT_PATH+"health_cpu"
	check_latency=config.CHECK_PATH+"./check_icmp -H %s -w %f -c %f -t %d > "%(config.cserver,config.lat_w,config.lat_c,config.lat_t)+config.OUTPUT_PATH+"health_latency"
	try:
		return_code=os.system(check_cpu)
	except:
		print "\nProcess",os.getpid(),"exiting now..."
		sys.exit()
	try:
		return_code=os.system(check_latency)
	except:
		print "\nProcess",os.getpid(),"exiting now..."
		sys.exit()
	result=get_output()
	save_result(result,start_time)
############################################################################################################################
# Fetches output from temp file.
############################################################################################################################
def get_output():
	file_cpu=open(config.OUTPUT_PATH+"health_cpu")
	file_latency=open(config.OUTPUT_PATH+"health_latency")
	out_list=[]
	for line in file_cpu:
		output=line.split('\n')
		out_list.append(output[0].split('|'))
	result={}
	if len(out_list)==1:
		perf_data=out_list[0][1]
	try:
		result['cpu_usage']=float(re.split('Total=|%',perf_data)[1])
	except:
		result['cpu_usage']=-1
	out_list=[]
	for line in file_latency:
		output=line.split('\n')
		out_list.append(output[0].split('|'))
	if len(out_list)==1:
		perf_data=out_list[0][1]
	try:
		result['latency']=float(re.split('rta=|ms',perf_data)[1])
	except:
		result['latency']=-1
	return result
############################################################################################################################
# Saves the result into database.
############################################################################################################################
def save_result(result,time):
	db=connect_db()
	cursor=db.cursor()
	query="""
				insert into Nocout_Health_Service
				( 
					probe_name,
					cpu_usage,
					latency,
					timestamp
				) values('%s',%f,%f,'%s')"""
	query%=(config.probe_name,\
			result['cpu_usage'],\
			result['latency'],\
			time)
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
# 
############################################################################################################################
