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

def postHealthDetails():
	probe_id=getProbe_id()
	if probe_id==-1:
		print "Probe ID not present in database."
		print "Exiting Now."
		sys.exit()
	db=MySQLdb.connect(config.probe_server,config.username,config.password,config.dbname)
	cursor=db.cursor(MySQLdb.cursors.DictCursor)
	sql="SELECT * from Nocout_Health_Service"

	'''Data Posting from client to central server'''
	try:
		cursor.execute(sql)
		result=cursor.fetchall()
		url=config.central_server+"HealthDetails/"
		for var in result:
			payload={}
			payload["Probe_ID"]=str(probe_id)
			payload["CPU_Usage"]=str(var["CPU_Usage"])
			payload["Ram_Usage"]=str(var["Latency"])
			payload["Timestanp"]=str(var["Timestamp"])
			headers = {'content-type': 'application/json','Accept': 'application/json'} #Content Type
			try:
				r=requests.post(url,data=json.dumps(payload),headers=headers) #requests
			except:
				print sys.exc_info()
				print "Connection Error..with status code %s"%(r.status_code)
			print r.status_code
			query="DELETE FROM Nocout_Health_Service where TIMESTAMP='%s'"%(var["Timestamp"])
			cursor.execute(query)
			db.commit()
	except:
		print sys.exc_info()
		print "Error : Health in Posting Data"
	db.close()
#postHealthDetails()
