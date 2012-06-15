from django.conf.urls.defaults import patterns, include, url
from app.views import ThingCreate, top, home

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mostawesome.views.home', name='home'),
    # url(r'^mostawesome/', include('mostawesome.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^add/$', ThingCreate.as_view(), name='thing_add'),
    url(r'^top/$', top, name='top'),
    url(r'^$', home, name='home')
)
