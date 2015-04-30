from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from webapp.views import CategoryViewSet


# Routers обеспечивают легкий способ автоматической генерации URL.
router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('webapp.urls')),
    url(r'^', include('loginsys.urls')),
	url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)