from django.conf.urls import patterns, include, url

urlpatterns = patterns('loginsys.views',
    url(r'^login/$','login'),
    url(r'^logout/$','logout'),
)