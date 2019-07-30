
"""
WSGI config for disasterinfosite project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "disasterinfosite.settings")

wsgi_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(wsgi_dir)

sys.path.append(os.path.join(root_dir, 'venv/lib/python3.7/site-packages'))
sys.path.append(root_dir)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
