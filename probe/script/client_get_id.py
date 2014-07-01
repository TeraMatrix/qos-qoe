#!/usr/bin/env python
import requests, json, config, MySQLdb, config, sys
def getID():
	st="probe?Probe_Name=" #Defining Path
	query=config.central_server+st+config.probe_name #Getting Path from config file and appending it with probe_name 
	print query
	try:
		data=json.loads((requests.get(query)).text);#getting Probe ID using response library
	except:
		print sys.exc_info()[0]
		print "Check connection with central server"
		return -1
	try:
		probe_id=int(data[0]["Probe_ID"])
	except:
		print "Sorry, you are not an authentic user."
		return -1
	try:
		db=MySQLdb.connect(config.probe_server,config.username,config.password,config.dbname)
	except:
		print sys.exc_info()[0]
		print "Database Connection Error..."
		return -1
	cursor=db.cursor()
	query="update probe_lock set status=%d where name='Probe_id'"%(probe_id)
	try:
		cursor.execute(query)
		db.commit()
		print "Prode ID Successfully retreived with ID %d"%(probe_id)
		return 1
	except:
		db.rollback()
		print sys.exc_info()
		print "Failed to Update Probe ID..."
		print "Probably check if you are registered, Check Database parameter, Check Connections with parameter"
		return -1
	db.close()

	
