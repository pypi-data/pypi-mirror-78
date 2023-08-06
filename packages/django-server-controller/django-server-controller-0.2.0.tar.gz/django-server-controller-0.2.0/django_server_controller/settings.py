import os
from django.conf import settings
from fastutils import fsutils


default_uwsgi_ini_file = os.path.abspath(os.path.join(settings.BASE_DIR, "wsgi.ini"))
default_uwsgi_bin = fsutils.first_exists_file(
    "~/bin/uwsgi",
    "./bin/uwsgi",
    "/usr/local/bin/uwsgi",
    "/usr/bin/uwsgi",
    "/bin/uwsgi",
    default="uwsgi",
    )

UWSGI_PROJECT_BASE = getattr(settings, "UWSGI_PROJECT_BASE", os.getcwd())
UWSGI_WEB_ROOT = getattr(settings, "UWSGI_WEB_ROOT", os.path.abspath(os.path.join(UWSGI_PROJECT_BASE, "./web/")))
UWSGI_LOGS_ROOT = getattr(settings, "UWSGI_LOGS_ROOT", os.path.abspath(os.path.join(UWSGI_PROJECT_BASE, "./logs/")))
UWSGI_PIDFILE = getattr(settings, "UWSGI_PIDFILE", os.path.abspath(os.path.join(UWSGI_PROJECT_BASE, "./uwsgi.pid")))
UWSGI_INI_FILE = getattr(settings, "UWSGI_INI_FILE", default_uwsgi_ini_file)
UWSGI_BIN = getattr(settings, "UWSGI_BIN", default_uwsgi_bin)
