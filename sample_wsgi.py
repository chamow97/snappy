import os
import sys

path = '/home/chamow/snappy'

if path not is sys.path:
	sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'snappy.settings'

from django.core.wsgi import get_wsgi_application
from django.contrib.statifiles.handlers import StaticFilesHandler
application = StaticFilesHandler(get_wsgi_application())