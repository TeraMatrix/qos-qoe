from celery import task
from Nocout.models import TimeStamp_Performance

@task()
def add(x,y):
	Timestamp_health=TimeStamp_Performance.objects.values_list('Overall_Value',flat=True).filter(TimeStamp = '2014-06-19 19:05:27',Service_Name='Ping')
	timestamp_dict = {'health':Timestamp_health}
	return timestamp_dict
