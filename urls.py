from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from tcc3.core import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tcc3.views.home', name='home'),
    # url(r'^tcc3/', include('tcc3.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    
    (r'^$',                     views.home_page),
    (r'^post/(\d+)/$',          views.post),
    
    (r'^posts/fetch/$',         views.fetch_posts),
    
    (r'^smoke/$',               views.smoke_test),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'F:/Dropbox/web/thecollegecartel/tcc3/static/'}),
    )
