import os, sys
sys.path.append('/root/public_html/python/tcc3')
sys.path.append('/root/public_html/python')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tcc3.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()