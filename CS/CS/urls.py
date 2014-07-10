from django.conf.urls import patterns, include, url
from Nocout import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('Nocout.urls')),
    url(r'^',include('api.urls')),
	url(r'^admin/', include(admin.site.urls))
)
