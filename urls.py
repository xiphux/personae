from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^personae/', include('personae.foo.urls')),
    (r'^characters/', include('personae.characters.urls')),
    (r'^characters_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/xiphux/webapps/personae/media/characters'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
