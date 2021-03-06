from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import login, logout_then_login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^personae/', include('personae.foo.urls')),
    (r'^characters/', include('personae.characters.urls')),
    (r'^characters_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/xiphux/webapps/personae/media/characters'}),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout_then_login),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
