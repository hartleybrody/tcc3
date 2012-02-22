from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from tcc3.core import views
from django.views.decorators.cache import cache_page

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
    
    
    (r'^$',                     cache_page(views.home_page, 60 * 15 ) ),
    (r'^post/(\d+)/$',          cache_page(views.post, 60 * 60 * 24) ),
    
    (r'^posts/fetch/$',         views.fetch_posts),
    
    (r'^smoke/$',               views.smoke_test),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'F:/Dropbox/web/thecollegecartel/tcc3/static/'}),
    )
