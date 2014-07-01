#! /usr/bin/python
import MySQLdb,os,re,sys,time,datetime,config
MegaBytes = 1024*1024
############################################################################################################################
# Connect to the Database
############################################################################################################################
def connect_db():
	try:
		return MySQLdb.connect(config.probe_server,config.username,config.password,config.dbname)
	except:
		print "DB connection error"
		sys.exit()
############################################################################################################################
# Calculate the Value for each services
############################################################################################################################
def calculate_Value(SVC_Name,data):
	cal_value = []	
	if SVC_Name == "HTTP":
		result =  re.split(';| |=',data)
		try:
			time = float(result[1][:-1])
		except:
			time = -1
		try:
			data = float(result[6][:-1])
		except:
			data =1
		if time!=-1 and data!=-1:
			cal_value.append(((data/MegaBytes)/time))
		else:
			cal_value.append(-1)
	elif SVC_Name == "ICMP":
		result = re.split(';| |=',data)
		try:
			RTA = float(result[1][:-2])
		except:
			RTA = -1
		try:
			Packet_Loss = float(result[7][:-1])
		except:
			Packet_Loss = -1
		cal_value.append(RTA)
		cal_value.append(Packet_Loss)		
	elif SVC_Name == "TCP":
		result = re.split(';| |=',data)
		try:
			Response_Time = float(result[1][:-1])*float(100)
		except:
			Response_Time = -1
		cal_value.append(Response_Time)	
	elif SVC_Name == "DNS":
		result = re.split(';| |=',data)
		try:
			Response_Time = float(result[1][:-1])*float(100)
		except:
			Response_Time = -1
		cal_value.append(Response_Time)	
	return cal_value
############################################################################################################################
# Insert the performance data for the particular Probe Services into Table
############################################################################################################################
def insert_perf_data(Service_ID,Probe_Name,SVC_Name,SVC_Param,perfdata,start_time):
	Value = calculate_Value(SVC_Name,perfdata)
	db = connect_db()
	cursor = db.cursor()
	SVC_Para = []
	if SVC_Name == "ICMP":
		SVC_Para.append("Avg. RTA")
		SVC_Para.append("Packet Loss")	
	elif SVC_Name == "HTTP":
		SVC_Para.append("Downlink")
	elif SVC_Name == "TCP":
		SVC_Para.append("Response Time")
	elif SVC_Name == "DNS":
		SVC_Para.append("Response Time")
	index = 0;
	for SVC_Param in SVC_Para:
		if Value[index]!=-1:
			query="""
					insert into Nocout_performance_services
					(
						service_id, 
						Probe_Name,	
						SVC_Name,
						SVC_Param,
						Timestamp,
						Value
					) values(%d,'%s','%s','%s','%s',%.6f)"""
			query%=(Service_ID,\
					Probe_Name,\
					SVC_Name,\
					SVC_Param,\
					start_time,\
					Value[index])
			try:
				cursor.execute(query)
				db.commit()
			except:
				db.rollback()
		index+=1
	db.close()
	return True
############################################################################################################################
# Delete the rows from the perf_data which is written in Performance_Service_Data
############################################################################################################################	
def delete_read_row(Service_ID,Start_Time):
	db = connect_db()
	cursor = db.cursor()	
	sql = " DELETE from perf_data WHERE start_time = '%s' AND service_id=%d" % (Start_Time,Service_ID)
	try:
		cursor.execute(sql)
		db.commit()
		db.close()
		return True
	except:
		db.rollback()
		db.close()
		return False
############################################################################################################################
# Read the data from the perf_data to deaggregate it
############################################################################################################################
def read_From_Db():
	db = connect_db()
	cursor = db.cursor()
	sql = " SELECT * FROM perf_data "
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			service_id		 = row[0]
			current_check_attempt 	 = row[1]
			max_check_attempt	 = row[2]
			start_time		 = row[3]
			end_time		 = row[4]
			timeout			 = row[5]
			execution_time		 = row[6]
			return_code		 = row[7]
			output			 = row[8]
			perfdata		 = row[9]
			SVC_name		 = row[10]
			SVC_Param		 = row[11]
			Target_IP 		 = row[12]
			Probe_Name		 = row[13]	
			insert_perf_data(service_id,Probe_Name,SVC_name,SVC_Param,perfdata,start_time)
			delete_read_row(service_id,start_time)
		db.close()
		return True
	except:
		db.close()
		return False
############################################################################################################################
# 
############################################################################################################################
