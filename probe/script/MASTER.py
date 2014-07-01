#!/usr/bin/env python
import time, client_get_id, MySQLdb, client_get_config, client_post_health,client_post_performance, sys, signal,config
from multiprocessing import Process
def getConfiguration():
	while True:
		db=MySQLdb.connect(config.probe_server,config.username,config.password,config.dbname)
		cursor=db.cursor()
		sql="DELETE FROM Nocout_Probe_Service_Conf"
		try:
			cursor.execute(sql)
			db.commit()
		except:
			print sys.exc_info()
			print "Error"
		db.close()
		client_get_config.getConfiguration()
		print "Configuration Updated"
		time.sleep(100)
	print "Configuration function exiting..."

def postHealthDetails():
	while True:
		client_post_health.postHealthDetails()
		time.sleep(10)
		print "Health Posted"
	print "Health function exiting..."
	

def postPerformance():
	while True:
		client_post_performance.postPerformance()
		time.sleep(10)
		print "Performance Posted"
	print "Performance function exiting..."
	
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

if __name__=="__main__":
	if(client_get_id.getID()==1):
		Configuration_Process=Process(target=getConfiguration).start()
		Health_Process=Process(target=postHealthDetails).start()
		Performance_Process=Process(target=postPerformance).start()
		signal.signal(signal.SIGINT, signal_handler)
		signal.pause()
		Configuration_Process.join();
		Health_Process.join();
		Performance_Process.join();
	else:
		print "Program Exiting..!! with status -1"




