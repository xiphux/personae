from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('personae.characters.views',
    # Example
    # (r'^personae/', include('personae.foo.urls')),
    (r'^new/$', 'newcharacter'),
    (r'^create/$', 'createcharacter'),
    (r'^(?P<character_id>\d+)/$', 'detail'),
    (r'^(?P<character_id>\d+)/edit/$', 'edit'),
    (r'^(?P<character_id>\d+)/new/$', 'newrevision'),
    (r'^(?P<character_id>\d+)/(?P<revision_id>)/$', 'viewrevision'),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
