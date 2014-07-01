#!/usr/bin/env python
import requests, json, MySQLdb, sys, config 


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


def postPerformance():
	probe_id=getProbe_id()
	if probe_id==-1:
		print "Probe ID not present in database."
		print "Exiting Now."
		sys.exit()
	
	db=MySQLdb.connect(config.probe_server,config.username,config.password,config.dbname)
	cursor=db.cursor(MySQLdb.cursors.DictCursor)
	sql="SELECT * from Nocout_performance_services"
	try:
		cursor.execute(sql)
		result=cursor.fetchall()
		url=config.central_server+"PerformanceDetails/"
		for var in result:
			payload={}
			payload["Service_ID"]=str(var["Service_id"])
			payload["Probe_ID"]=str(probe_id)
			payload["SVC_Name"]=str(var["SVC_Name"])
			payload["SVC_Param"]=str(var["SVC_Param"])
			payload["Value"]=str(var["Value"])
			payload["TimeStamp"]=str(var["Timestamp"])
			headers = {'content-type': 'application/json','Accept': 'application/json'}
			try:
				r=requests.post(url,data=json.dumps(payload),headers=headers)
			except:
				print "Error in Connection..with status code %s"%(r.status_code)
			print "Performance posted %s"%(r.status_code)
			query="DELETE FROM Nocout_performance_services where TIMESTAMP='%s' AND Service_ID='%d'" %(var["Timestamp"],var["Service_id"])
			cursor.execute(query)
			db.commit()
	except:
		print sys.exc_info()
		print "Error : In posting Performance"
	db.close()
#postPerformance()
