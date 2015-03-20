from django.conf.urls import patterns, url

from webapp import views

urlpatterns = patterns('',
    # ex: /webapp/
    url(r'^$', views.index, name='index'),
    # ex: /webapp/5/
    url(r'^(?P<post_id>\d+)/$', views.detail, name='detail'),
)