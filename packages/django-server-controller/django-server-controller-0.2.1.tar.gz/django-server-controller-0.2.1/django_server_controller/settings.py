import os
from django.conf import settings
from fastutils import fsutils

UWSGI_PROJECT_BASE = getattr(settings, "UWSGI_PROJECT_BASE", os.getcwd())


def get_default_uwsgi_ini_file():
    return fsutils.first_exists_file(
        os.path.abspath(os.path.join(UWSGI_PROJECT_BASE, "./etc/wsgi.ini")),
        "./etc/wsgi.ini",
        "~/etc/wsgi.ini",
        default=os.path.abspath(os.path.join(settings.BASE_DIR, "wsgi.ini"))
    )
 
def get_default_uwsgi_bin():
    return fsutils.first_exists_file(
        os.path.abspath(os.path.join(UWSGI_PROJECT_BASE, "./bin/uwsgi")),
        "./bin/uwsgi",
        "~/bin/uwsgi",
        "/usr/local/bin/uwsgi",
        "/usr/bin/uwsgi",
        "/bin/uwsgi",
        default="uwsgi",
    )

UWSGI_WEB_ROOT = getattr(settings, "UWSGI_WEB_ROOT", os.path.abspath(os.path.join(UWSGI_PROJECT_BASE, "./web/")))
UWSGI_LOGS_ROOT = getattr(settings, "UWSGI_LOGS_ROOT", os.path.abspath(os.path.join(UWSGI_PROJECT_BASE, "./logs/")))
UWSGI_PIDFILE = getattr(settings, "UWSGI_PIDFILE", os.path.abspath(os.path.join(UWSGI_PROJECT_BASE, "./uwsgi.pid")))
UWSGI_INI_FILE = getattr(settings, "UWSGI_INI_FILE", get_default_uwsgi_ini_file())
UWSGI_BIN = getattr(settings, "UWSGI_BIN", get_default_uwsgi_bin())
