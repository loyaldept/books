"""
WSGI config for library_management project by @Zuhayr Abdullazhanov
materials used: Stackoverflow
It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')
application = get_wsgi_application()
