from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^webapp/', include('webapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
)