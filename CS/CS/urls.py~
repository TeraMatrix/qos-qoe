from django.conf.urls import patterns, include, url
from Nocout import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('Nocout.urls')),
    url(r'^',include('api.urls')),
	url(r'^admin/', include(admin.site.urls))
)
