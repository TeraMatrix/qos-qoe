'''Url file of Django
It list all the endpoints available for probe'''

from django.conf.urls import patterns, url
from api import views
urlpatterns = patterns('api.views',
    url(r'^api/configuration/$', views.ConfigDetails.as_view()),
    url(r'^api/HealthDetails/$', views.HealthDetails.as_view()),
    url(r'^api/PerformanceDetails/$', views.PerformanceDetails.as_view()),
	url(r'^api/probe/$',views.ProbeList.as_view()),
)
