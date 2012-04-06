import os, sys
sys.path.append('/root/tcc3')
sys.path.append('/root')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tcc3.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()