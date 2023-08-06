
import os
import time
import click
import psutil
from fastutils import fsutils



class UwsgiController(object):

    @classmethod
    def get_default_project_base(cls):
        return os.getcwd()
    
    @classmethod
    def get_default_web_root(cls, project_base):
        return os.path.abspath(os.path.join(project_base, "./web/"))
    
    @classmethod
    def get_default_logs_root(cls, project_base):
        return os.path.abspath(os.path.join(project_base, "./logs/"))

    @classmethod
    def get_default_pidfile(cls, project_base):
        return os.path.abspath(os.path.join(project_base, "./uwsgi.pid"))

    @classmethod
    def get_default_uwsgi_bin(cls):
        return fsutils.first_exists_file(
            "~/bin/uwsgi",
            "./bin/uwsgi",
            "/usr/local/bin/uwsgi",
            "/usr/bin/uwsgi",
            "/bin/uwsgi",
            default="uwsgi",
        )

    def __init__(self, project_base, uwsgi_ini_file, web_root=None, logs_root=None, pidfile=None, uwsgi_bin=None):
        self.project_base = project_base
        os.chdir(self.project_base)

        self.uwsgi_ini_file = uwsgi_ini_file
        self.web_root = web_root or self.get_default_web_root(self.project_base)
        self.logs_root = logs_root or self.get_default_logs_root(self.project_base)
        self.pidfile = pidfile or self.get_default_pidfile(self.project_base)
        self.uwsgi_bin = uwsgi_bin or self.get_default_uwsgi_bin()

    def get_server_pid(self):
        if not os.path.isfile(self.pidfile):
            return 0
        with open(self.pidfile, "r", encoding="utf-8") as fobj:
            return int(fobj.read().strip())

    def get_running_server_pid(self):
        pid = self.get_server_pid()
        if not pid:
            return 0
        if psutil.pid_exists(pid):
            return pid
        else:
            return 0

    def start(self):
        """Start uwsgi server.
        """
        os.chdir(self.web_root)
        pid = self.get_running_server_pid()
        if pid:
            pid = self.get_server_pid()
            print("Uwsgi service is running: {}...".format(pid))
            os.sys.exit(1)
        else:
            print("Start uwsgi server...")
            cmd = "{0} {1}".format(self.uwsgi_bin, self.uwsgi_ini_file)
            print(cmd)
            os.system(cmd)
            print("Uwsgi server started!")

    def stop(self):
        """Stop uwsgi server.
        """
        os.chdir(self.web_root)
        pid = self.get_running_server_pid()
        if pid:
            print("Stop uwsgi server...")
            cmd = "{0} --stop {1}".format(self.uwsgi_bin, self.pidfile)
            print(cmd)
            os.system(cmd)
            print("Uwsgi server stopped!")
        else:
            print("Uwsgi service is NOT running!")


    def reload(self):
        """Reload uwsgi server.
        """
        os.chdir(self.web_root)
        pid = self.get_running_server_pid()
        if pid:
            print("Reload uwsgi server...")
            cmd = "{0} --reload {1}".format(self.uwsgi_bin, self.pidfile)
            print(cmd)
            os.system(cmd)
            print("Uwsgi server reloaded!")
        else:
            print("Uwsgi service is NOT running, try to start it!")
            self.start()

    def restart(self, wait_seconds=2):
        """Restart uwsgi server.
        """
        self.stop()
        if wait_seconds:
            time.sleep(wait_seconds)
        self.start()

    def status(self):
        """Get uwsgi server status.
        """
        os.chdir(self.web_root)
        pid = self.get_running_server_pid()
        if pid:
            print("Uwsgi server is running: {0}.".format(pid))
        else:
            print("Uwsgi server is NOT running.")

    def get_controller(self):

        @click.group()
        def main():
            pass

        @main.command()
        def reload():
            """Reload uwsgi server.
            """
            self.reload()

        @main.command()
        @click.option("-w", "--wait-seconds", type=int, default=2, help="Wait some seconds after stop and before start the uwsgi server.")
        def restart(wait_seconds):
            """Restart uwsgi server.
            """
            self.restart(wait_seconds)


        @main.command()
        def start():
            """Start uwsgi server.
            """
            self.start()

        @main.command()
        def stop():
            """Stop uwsgi server.
            """
            self.stop()

        @main.command()
        def status():
            """Get uwsgi server's status.
            """
            self.status()

        return main