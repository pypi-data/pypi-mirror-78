import os
import djclick as click
from django_server_controller import settings
from django_server_controller import controllers

def get_wsgi_controller():
    return controllers.UwsgiController(
        project_base=settings.UWSGI_PROJECT_BASE,
        uwsgi_ini_file=settings.UWSGI_INI_FILE,
        web_root=settings.UWSGI_WEB_ROOT,
        logs_root=settings.UWSGI_LOGS_ROOT,
        pidfile=settings.UWSGI_PIDFILE,
        uwsgi_bin=settings.UWSGI_BIN,
    )

@click.group()
def main():
    pass

@main.command()
def reload():
    """Reload uwsgi server.
    """
    ctrl = get_wsgi_controller()
    ctrl.reload()

@main.command()
@click.option("-w", "--wait-seconds", type=int, default=2, help="Wait some seconds after stop and before start the uwsgi server.")
def restart(wait_seconds):
    """Restart uwsgi server.
    """
    ctrl = get_wsgi_controller()
    ctrl.restart(wait_seconds)


@main.command()
def start():
    """Start uwsgi server.
    """
    ctrl = get_wsgi_controller()
    ctrl.start()

@main.command()
def stop():
    """Stop uwsgi server.
    """
    ctrl = get_wsgi_controller()
    ctrl.stop()

@main.command()
def status():
    """Get uwsgi server's status.
    """
    ctrl = get_wsgi_controller()
    ctrl.status()

if __name__ == "__main__":
    main()
